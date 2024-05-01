# model.py
# https://github.com/ddh0/easy-llama/

"""Submodule containing the Model class to work with language models"""

from typing     import Generator, Optional, TextIO, Union, List
from .utils     import GGUFReader, print_warning, print_verbose
from .samplers  import SamplerSettings, DefaultSampling
from llama_cpp  import Llama, StoppingCriteriaList
from os.path    import isdir, exists

from os  import cpu_count as os_cpu_count
from sys import stdout    as sys_stdout


# for typing of Model.stream_print() parameter `file`
class _SupportsWriteAndFlush(TextIO):
    pass

class ModelUnloadedException(Exception):
    """Exception raised when trying to use a Model that has been unloaded"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        self.add_note('Are you trying to use a Model that has been unloaded?')

class Model:
    """
    A high-level abstraction of a llama model

    This is just a brief overview of easy_llama.Model.
    To see a full description of each method and its parameters,
    call help(Model), or see the relevant docstring.

    The following methods are available:
    - `.generate()` - Generate text
    - `.get_length()` - Get the length of a given text in tokens
    - `.ingest()` - Ingest text into the model's cache
    - `.next_candidates()` - Get a list of the most likely next tokens (WIP)
    - `.stream()` - Return a Generator that can stream text as it is generated
    - `.stream_print()` - Print text as it is generated
    - `.trim()` - Trim a given text to the model's context length
    - `.unload()` - Unload the model from memory

    The following attributes are available:
    - `.bos_token` - The model's beginning-of-stream token ID
    - `.context_length` - The model's loaded context length
    - `.eos_token` - The model's end-of-stream token ID
    - `.llama` - The underlying `llama_cpp.Llama` instance
    - `.metadata` - The GGUF metadata of the model
    - `.n_ctx_train` - The native context length of the model
    - `.rope_freq_base` - The model's loaded RoPE frequency base
    - `.rope_freq_base_train` - The model's native RoPE frequency base
    - `.tokens` - A list of all the tokens in the model's tokenizer
    - `.verbose` - Whether or not the model was loaded with `verbose=True`
    """

    def __init__(
            self,
            model_path: str,
            context_length: Optional[int] = None,
            n_gpu_layers: int = 0,
            offload_kqv: bool = True,
            verbose: bool = False
        ):
        """
        Given the path to a GGUF file, construct a Model instance.

        The model must be in GGUF format.

        The following parameters are optional:
        - context_length: The context length at which to load the model, in tokens
        - n_gpu_layers: The number of layers to be offloaded to the GPU
        - offload_kqv: Whether or not the KQV cache (context) should be offloaded
        - verbose: Whether or not to print additional backend information
        """

        assert isinstance(model_path, str), \
            f"Model: model_path should be a string, not {type(model_path)}"
        assert exists(model_path), \
            f"Model: the given model_path '{model_path}' does not exist"
        assert not isdir(model_path), \
            f"Model: the given model_path '{model_path}' is a directory, not a GGUF file"
        assert isinstance(context_length, (int, type(None))), \
            f"Model: context_length should be int or None, not {type(context_length)}"
        
        # save __init__ parameters for __repr__
        self._model_path = model_path
        self._context_length = context_length
        self._n_gpu_layers = n_gpu_layers
        self._offload_kqv = offload_kqv
        self._verbose = self.verbose = verbose

        # if context_length <= 0, use n_ctx_train
        if isinstance(context_length, int) and context_length <= 0:
            context_length = None

        # this does not use Llama.metadata because we want to use GGUF
        # metadata to determine some parameters of the Llama instance
        # before it is created
        self.metadata = GGUFReader.load_metadata(self, model_path)
        metadata_keys = self.metadata.keys() # only read once

        n_ctx_train = None
        for key in metadata_keys:
            if key.endswith('.context_length'):
                n_ctx_train = self.metadata[key]
                break

        if n_ctx_train is None:
            raise KeyError(
                "GGUF file does not specify a context length"
            )
        
        rope_freq_base_train = None
        for key in metadata_keys:
            if key.endswith('.rope.freq_base'):
                rope_freq_base_train = self.metadata[key]
                break

        if rope_freq_base_train is None and context_length is not None:
            if context_length > n_ctx_train:
                raise ValueError(
                    'unable to load model with greater than native ' + \
                    f'context length ({context_length} > {n_ctx_train}) ' + \
                    'because model does not specify freq_base. ' + \
                    f'try again with `context_length={n_ctx_train}`'
                )

        if rope_freq_base_train is None or context_length is None or \
            context_length <= n_ctx_train:
            # no need to do context scaling, load model normally

            if context_length is None:
                self.context_length = n_ctx_train
            else:
                self.context_length = context_length
            rope_freq_base = rope_freq_base_train

        elif context_length > n_ctx_train:
            # multiply rope_freq_base according to requested context length
            # because context length > n_ctx_train and rope freq base is known

            rope_freq_base = (context_length/n_ctx_train)*rope_freq_base_train
            self.context_length = context_length
            
            if self.verbose:
                print_verbose(
                    'chosen context length is greater than native context '
                    f'length ({context_length} > {n_ctx_train}), ' + \
                    'rope_freq_base will be changed from ' + \
                    f'{rope_freq_base_train} to {rope_freq_base}'
                )

            if 2 <= context_length/n_ctx_train < 4:
                print_warning(
                    'loading model with 2x native context length or more, ' + \
                    'expect small loss of quality'
                )
            
            elif 4 <= context_length/n_ctx_train < 8:
                print_warning(
                    'loading model with 4x native context length or more, ' + \
                    'expect moderate loss of quality'
                )

            elif context_length/n_ctx_train >= 8:
                print_warning(
                    'loading model with 8x native context length or more, ' + \
                    'expect SIGNIFICANT loss of quality'
                )
        
        # expose these values because they may be useful / informative
        self.n_ctx_train = n_ctx_train
        self.rope_freq_base_train = rope_freq_base_train
        self.rope_freq_base = rope_freq_base
        
        try:
            self.tokens: List[str] = self.metadata['tokenizer.ggml.tokens']
        except KeyError:
            print_warning(
                "could not set Model.tokens, defaulting to None"
            )
            self.tokens = None
        try:
            self.bos_token: int = self.metadata['tokenizer.ggml.bos_token_id']
        except KeyError:
            print_warning(
                "could not set Model.bos_token, defaulting to None"
            )
            self.bos_token = None
        try:
            self.eos_token: int = self.metadata['tokenizer.ggml.eos_token_id']
        except KeyError:
            print_warning(
                "could not set Model.eos_token, defaulting to None"
            )
            self.eos_token = None

        cpu_count = os_cpu_count()

        # these values for n_threads and n_threads_batch are
        # known to be optimal for most systems
        n_batch = 512 # can this be optimized?
        n_threads = max(cpu_count//2, 1)
        n_threads_batch = cpu_count

        self.llama: Llama = Llama(
            model_path=model_path,
            n_ctx=self.context_length,
            n_gpu_layers=n_gpu_layers,
            use_mmap=True,
            use_mlock=False,
            logits_all=False,
            n_batch=n_batch,
            n_threads=n_threads,
            n_threads_batch=n_threads_batch,
            rope_freq_base=rope_freq_base,
            mul_mat_q=True,
            offload_kqv=offload_kqv,
            # KV cache quantization
            # use 1 for F16 (default), 8 for q8_0, 2 for q4_0, 3 for q4_1
            #type_k=8,
            #type_v=8,
            verbose=verbose
        )
        
        # once model is loaded, replace metadata (as read using internal class)
        # with metadata (as read using the more robust llama-cpp-python code) 
        self.metadata = self.llama.metadata

        if self.verbose:
            print_verbose("new Model instance with the following attributes:")
            print_verbose(f"model: {model_path}")
            print_verbose(f"param: n_gpu_layers         == {n_gpu_layers}")
            print_verbose(f"param: offload_kqv          == {offload_kqv}")
            print_verbose(f"param: n_batch              == {n_batch}")
            print_verbose(f"param: n_threads            == {n_threads}")
            print_verbose(f"param: n_threads_batch      == {n_threads_batch}")
            print_verbose(f" gguf: n_ctx_train          == {n_ctx_train}")
            print_verbose(f"param: self.context_length  == {self.context_length}")
            print_verbose(f" gguf: rope_freq_base_train == {rope_freq_base_train}")
            print_verbose(f"param: rope_freq_base       == {rope_freq_base}")
    
    def __repr__(self) -> str:
        return \
            f"Model({repr(self._model_path)}, " + \
            f"context_length={self._context_length}, " + \
            f"n_gpu_layers={self._n_gpu_layers}, " + \
            f"offload_kqv={self._offload_kqv}, "+ \
            f"verbose={self._verbose})"

    def __del__(self):
        self.unload()
    
    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.unload()
    
    def __call__(
            self,
            prompt: Union[str, list[int]],
            stops: list[Union[str, int]] = [],
            sampler: SamplerSettings = DefaultSampling
        ) -> str:
        """
        `Model(...)` is a shorthand for `Model.generate(...)`
        """
        return self.generate(prompt, stops, sampler)

    def unload(self):
        """
        Unload the model from memory
        """
        # ref: llama_cpp._internals._LlamaModel.__del__()
        if not hasattr(self, 'llama'):
            # model already unloaded, do nothing
            return
        try:
            # actually unload the model from memory
            self.llama._model._llama_free_model(self.llama._model.model)
            self.llama._model.model = None
        except AttributeError:
            # broken or already being destoryed by GC, abort
            return
        if hasattr(self, 'llama'):
            delattr(self, 'llama')
        if self.verbose:
            print_verbose('Model unloaded')
    
    def trim(self,
             text: str,
             overwrite: Optional[str] = None
        ) -> str:

        """
        Trim the given text to the context length of this model,
        leaving room for two extra tokens.

        Optionally overwrite the oldest tokens with the text given in the
        `overwrite` parameter, which may be useful for keeping some
        information in context.

        Does nothing if the text is equal to or shorter than
        (context_length - 2).
        """
        assert_model_is_loaded(self)
        trim_length = self.context_length - 2
        tokens_list = self.llama.tokenize(
            text.encode("utf-8", errors="ignore")
        )

        if len(tokens_list) <= trim_length:
            if overwrite is not None:
                text[0 : len(overwrite)] = overwrite
            return text

        if len(tokens_list) > trim_length and overwrite is None:
            # cut to trim_length
            tokens_list = tokens_list[-trim_length:]
            return self.llama.detokenize(tokens_list).decode(
                "utf-8",
                errors="ignore"
            )

        if len(tokens_list) > trim_length and overwrite is not None:
            # cut to trim_length
            tokens_list = tokens_list[-trim_length:]
            overwrite_tokens = self.llama.tokenize(overwrite.encode(
                "utf-8",
                errors="ignore"
                )
            )
            # overwrite oldest tokens
            tokens_list[0 : len(overwrite_tokens)] = overwrite_tokens
            return self.llama.detokenize(tokens_list).decode(
                "utf-8",
                errors="ignore"
            )

    def get_length(self, text: str) -> int:
        """
        Return the length of the given text in tokens according to this model,
        including the appended BOS token.
        """
        assert_model_is_loaded(self)
        return len(self.llama.tokenize(
            text.encode(
                "utf-8",
                errors="ignore"
                )
            ))

    def generate(
            self,
            prompt: Union[str, list[int]],
            stops: list[Union[str, int]] = [],
            sampler: SamplerSettings = DefaultSampling
            ) -> str:
        """
        Given a prompt, return a generated string.

        prompt: The text from which to generate

        The following parameters are optional:
        - stops: A list of strings and/or token IDs at which to end the generation early
        - sampler: The SamplerSettings object used to control text generation
        """

        assert isinstance(prompt, (str, list)), \
            f"generate: prompt should be string or list[int], not {type(prompt)}"
        if isinstance(prompt, list):
            assert all(isinstance(tok, int) for tok in prompt), \
                "generate: some token in prompt is not an integer"
        assert isinstance(stops, list), \
            f"generate: parameter `stops` should be a list, not {type(stops)}"
        assert all(isinstance(item, (str, int)) for item in stops), \
            f"generate: some item in parameter `stops` is not a string or int"

        if self.verbose:
            print_verbose(f'using the following sampler settings for Model.generate:')
            print_verbose(f'max_len_tokens    == {sampler.max_len_tokens}')
            print_verbose(f'temp              == {sampler.temp}')
            print_verbose(f'top_p             == {sampler.top_p}')
            print_verbose(f'min_p             == {sampler.min_p}')
            print_verbose(f'frequency_penalty == {sampler.frequency_penalty}')
            print_verbose(f'presence_penalty  == {sampler.presence_penalty}')
            print_verbose(f'repeat_penalty    == {sampler.repeat_penalty}')
            print_verbose(f'top_k             == {sampler.top_k}')

        # if any stop item is a token ID (int)
        if any(isinstance(stop, int) for stop in stops):
            # stop_strs is a list of all stopping strings
            stop_strs: list[str] = [stop for stop in stops if isinstance(stop, str)]
            # stop_token_ids is a list of all stop token IDs
            stop_token_ids: list[int] = [tok_id for tok_id in stops if isinstance(tok_id, int)]
            def stop_on_token_ids(tokens, *args, **kwargs):
                return tokens[-1] in stop_token_ids
            stopping_criteria = StoppingCriteriaList([stop_on_token_ids])
            assert_model_is_loaded(self)
            return self.llama.create_completion(
                prompt,
                max_tokens=sampler.max_len_tokens,
                temperature=sampler.temp,
                top_p=sampler.top_p,
                min_p=sampler.min_p,
                frequency_penalty=sampler.frequency_penalty,
                presence_penalty=sampler.presence_penalty,
                repeat_penalty=sampler.repeat_penalty,
                top_k=sampler.top_k,
                stop=stop_strs,
                stopping_criteria=stopping_criteria
            )['choices'][0]['text']

        # if stop items are only strings
        assert_model_is_loaded(self)
        return self.llama.create_completion(
            prompt,
            max_tokens=sampler.max_len_tokens,
            temperature=sampler.temp,
            top_p=sampler.top_p,
            min_p=sampler.min_p,
            frequency_penalty=sampler.frequency_penalty,
            presence_penalty=sampler.presence_penalty,
            repeat_penalty=sampler.repeat_penalty,
            top_k=sampler.top_k,
            stop=stops
        )['choices'][0]['text']
    

    def stream(
            self,
            prompt: Union[str, list[int]],
            stops: list[Union[str, int]] = [],
            sampler: SamplerSettings = DefaultSampling
        ) -> Generator:

        """
        Given a prompt, return a generator that yields dicts containing tokens.

        To get the token string itself, subscript the dict with:

        `['choices'][0]['text']`

        prompt: The text from which to generate

        The following parameters are optional:
        - stops: A list of strings and/or token IDs at which to end the generation early
        - sampler: The SamplerSettings object used to control text generation
        """

        assert isinstance(prompt, (str, list)), \
            f"stream: prompt should be string or list[int], not {type(prompt)}"
        if isinstance(prompt, list):
            assert all(isinstance(tok, int) for tok in prompt), \
                "stream: some token in prompt is not an integer"
        assert isinstance(stops, list), \
            f"stream: parameter `stops` should be a list, not {type(stops)}"
        assert all(isinstance(item, (str, int)) for item in stops), \
            f"stream: some item in parameter `stops` is not a string or int"

        if self.verbose:
            print_verbose(f'using the following sampler settings for Model.stream:')
            print_verbose(f'max_len_tokens    == {sampler.max_len_tokens}')
            print_verbose(f'temp              == {sampler.temp}')
            print_verbose(f'top_p             == {sampler.top_p}')
            print_verbose(f'min_p             == {sampler.min_p}')
            print_verbose(f'frequency_penalty == {sampler.frequency_penalty}')
            print_verbose(f'presence_penalty  == {sampler.presence_penalty}')
            print_verbose(f'repeat_penalty    == {sampler.repeat_penalty}')
            print_verbose(f'top_k             == {sampler.top_k}')
        
        # if any stop item is a token ID (int)
        if any(isinstance(stop, int) for stop in stops):
            # stop_strs is a list of all stopping strings
            stop_strs: list[str] = [stop for stop in stops if isinstance(stop, str)]
            # stop_token_ids is a list of all stop token IDs
            stop_token_ids: list[int] = [tok_id for tok_id in stops if isinstance(tok_id, int)]
            def stop_on_token_ids(tokens, *args, **kwargs):
                return tokens[-1] in stop_token_ids
            stopping_criteria = StoppingCriteriaList([stop_on_token_ids])
            assert_model_is_loaded(self)
            return self.llama.create_completion(
                prompt,
                max_tokens=sampler.max_len_tokens,
                temperature=sampler.temp,
                top_p=sampler.top_p,
                min_p=sampler.min_p,
                frequency_penalty=sampler.frequency_penalty,
                presence_penalty=sampler.presence_penalty,
                repeat_penalty=sampler.repeat_penalty,
                top_k=sampler.top_k,
                stream=True,
                stop=stop_strs,
                stopping_criteria=stopping_criteria
            )

        assert_model_is_loaded(self)
        return self.llama.create_completion(
            prompt,
            max_tokens=sampler.max_len_tokens,
            temperature=sampler.temp,
            top_p=sampler.top_p,
            min_p=sampler.min_p,
            frequency_penalty=sampler.frequency_penalty,
            presence_penalty=sampler.presence_penalty,
            repeat_penalty=sampler.repeat_penalty,
            top_k=sampler.top_k,
            stream=True,
            stop=stops
        )


    def stream_print(
            self,
            prompt: Union[str, list[int]],
            stops: list[Union[str, int]] = [],
            sampler: SamplerSettings = DefaultSampling,
            end: str = "\n",
            file: _SupportsWriteAndFlush = sys_stdout,
            flush: bool = True
    ) -> str:
        """
        Given a prompt, stream text as it is generated, and return the generated string.
        The returned string does not include the `end` parameter.

        `Model.stream_print(...)` is a shorthand for:
        ```
        s = Model.stream(prompt, stops=stops, sampler=sampler)
        for i in s:
            tok = i['choices'][0]['text']
            print(tok, end='', file=file, flush=flush)
        print(end, end='', file=file, flush=True)
        ```

        prompt: The text from which to generate

        The following parameters are optional:
        - stops: A list of strings and/or token IDs at which to end the generation early
        - sampler: The SamplerSettings object used to control text generation
        - end: A string to print after the generated text
        - file: The file where text should be printed
        - flush: Whether to flush the stream after each token
        """
        
        token_generator = self.stream(
            prompt=prompt,
            stops=stops,
            sampler=sampler
        )

        res = ''
        for i in token_generator:
            tok = i['choices'][0]['text']
            print(tok, end='', file=file, flush=flush)
            res += tok

        # always flush stream after generation is done
        print(end, end='', file=file, flush=True)

        return res


    def ingest(self, text: str) -> None:
        """
        Ingest the given text into the model's cache
        """

        assert_model_is_loaded(self)
        self.llama.create_completion(
            text,
            max_tokens=1,
            temperature=0.0
        )
    

    def next_candidates(
            self,
            prompt: str,
            k: int
        ) -> list[str]:
        """
        Given prompt `str` and k `int`, return a sorted list of the
        top k candidates for most likely next token
        """
        # WIP
        raise NotImplementedError(
            'Model.next_candidates() is not yet implemented'
        )
        assert_model_is_loaded(self)
        tokens = self.llama.tokenize(prompt.encode('utf-8', errors='ignore'))
        self.llama.eval(tokens)
        self.llama.scores

def assert_model_is_loaded(model: Model) -> None:
    """
    Ensure the Model is fully constructed, such that
    `Model.llama._model.model is not None` is guaranteed to be `True`

    Raise ModelUnloadedException otherwise
    """
    if not hasattr(model, 'llama'):
        raise ModelUnloadedException(
            "easy_llama.Model instance has no attribute 'llama'"
        )
    if not hasattr(model.llama, '_model'):
        raise ModelUnloadedException(
            "llama_cpp.Llama instance has no attribute '_model'"
        )
    if not hasattr(model.llama._model, 'model'):
        raise ModelUnloadedException(
            "llama_cpp._internals._LlamaModel instance has no attribute 'model'"
        )
    if model.llama._model.model is None:
        raise ModelUnloadedException(
            "llama_cpp._internals._LlamaModel.model is None"
        )

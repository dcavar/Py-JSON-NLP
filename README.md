# Python JSON-NLP Module

(C) 2020 by [Semiring Inc.]

Contributions from [Damir Cavar], [Oren Baldinger], [Maanvitha Gongalla], [Anurag Kumar], Murali Kammili, and others during 2019.

Brought to you by the [NLP-Lab.org]. New Maintainer since 2020 is [Semiring Inc.].

This new version now is 0.6 and it is no longer compatible with version 0.2.33. If you use the old JSON-NLP standard in your code, make sure you require version 0.2.33 of *pyjsonnlp*. This new version is compatible with the newest version of [Go JSON-NLP].



## Introduction

There is a growing number of Natural Language Processing (NLP) tools, modules, pipelines. There does not seem to be any standard for the output format. Here we are focusing on a standard for the output format syntax. Some future version of [JSON-NLP] might address the output semantics as well.

[JSON-NLP] is a standard for the most important outputs NLP pipelines and components can generate. The relevant documentation can be found in the [JSON-NLP] GitHub repo and on its website at the [NLP-Lab] and [Semiring Inc.].

The Python [JSON-NLP] module contains general mapping functions for [JSON-NLP] to [CoNLL-U], a validator for the generated output, an NLP pipeline interface (for [Flair], [spaCy], [NLTK], [Polyglot], [Xrenner], etc.), and various utility functions.

There is a [Java JSON-NLP](https://github.com/dcavar/J-JSON-NLP) Maven module as well, and there are wrappers for numerous popular NLP pipelines and tools linked from the [NLP-Lab.org] website.


## Installation

For more details, see [JSON-NLP].

This module is a wrapper for outputs from different NLP pipelines and modules into a standardized [JSON-NLP] format.

To install this package, run the following command:

    pip install pyjsonnlp

You might have to use *pip3* on some systems.


## Validation

[JSON-NLP] is based on a schema, maintained by [NLP-Lab.org] and [Semiring Inc.], to comprehensively and concisely represent linguistic annotations. 

We provide a validator to help ensure that generated JSON validates against the schema:

    result = MyPipeline().proces(text="I am a sentence")
    assert pyjsonnlp.validation.is_valid(result)


## Conversion

To enable interoperability with other annotation formats, we support conversions between them.
Note that conversion could be lossy, if the relative depths of annotation are not the same.
Currently we have a [CoNLL-U] to [JSON-NLP] converter, that covers most annotations:

    pyjsonnlp.conversion.parse_conllu(conllu_text)
    
To convert the other direction:

    pyjsonnlp.conversion.to_conllu(jsonnlp)


## Pipeline

[JSON-NLP] provides a simple `Pipeline` interface that should be implemented for embedding into a microservice:
    
    from collections import OrderedDict

    class MockPipeline(pyjsonnlp.pipeline.Pipeline):
        @staticmethod
        def process(text='', coreferences=False, constituents=False, dependencies=False, expressions=False,
                    **kwargs) -> OrderedDict: 
            return OrderedDict()
            
The provided keyword arguments should be used to toggle on or off processing components within the method.        
            
If you have deployed a `Pipeline` as a microservice (see below), we provide a local endpoint for a remotely 
deployed `Pipeline` via the `RemotePipeline` class:

    pipeline = pyjsonnlp.pipeline.RemotePipeline('localhost', port=9000)
    print(pipeline.process(text='I am a sentence', dependencies=True, something='else'), spacing=2)


## Microservice

The [JSON-NLP] as a Microservice class is only available in older versions of this module. Version 0.2.x is implemented as a Microsorvice with a pre-built implementation of [Flask].

    from pyjsonnlp.microservices.flask_server import FlaskMicroservice

    app = FlaskMicroservice(__name__, MyPipeline(), base_route='/')
 
We recommend creating a `server.py` with the `FlaskMicroservice` class, which extends the [Flask] app. A corresponding WSGI file would contain:

    from mypipeline.server import app as application
    
To disable a pipeline component (such as phrase structure parsing), add

    application.constituents = False
    
The full list of properties available that can be disabled or enabled are
- constituents
- dependencies
- coreference
- expressions

The microservice exposes the following URIs:
- /constituents
- /dependencies
- /coreference
- /expressions
- /token_list

These URIs are shortcuts to disable the other components of the parse. In all cases, `tokenList` will be included in the `JSON-NLP` output. An example url is:

    http://localhost:5000/dependencies?text=I am a sentence

Text is provided to the microservice with the `text` parameter, via either `GET` or `POST`. If you pass `url` as a parameter, the microservice will scrape that url and process the text of the website.

Other parameters specific to your pipeline implementation can be passed as well:

    http://localhost:5000?lang=en&constituents=0&text=I am a sentence.

The current version 0.6 or newer does not support the [Flask]-based RESTful Microservice infrastructure. It is a pure [JSON-NLP] data structure, processor and converter.



[Damir Cavar]: https://www.linkedin.com/in/damircavar/ "Damir Cavar"
[Oren Baldinger]: https://oren.baldinger.me/ "Oren Baldinger"
[Anurag Kumar]: https://github.com/anuragkumar95/ "Anurag Kumar"
[Maanvitha Gongalla]: https://maanvithag.github.io/MaanvithaGongalla/
[NLP-Lab.org]: http://nlp-lab.org/ "NLP-Lab.org"
[JSON-NLP]: https://github.com/SemiringInc/JSON-NLP "JSON-NLP"
[Flair]: https://github.com/zalandoresearch/flair "Flair"
[spaCy]: https://spacy.io/ "spaCy"
[NLTK]: http://nltk.org/ "Natural Language Processing Toolkit"
[Polyglot]: https://github.com/aboSamoor/polyglot "Polyglot" 
[Xrenner]: https://github.com/amir-zeldes/xrenner "Xrenner"
[CoNLL-U]: https://universaldependencies.org/format.html "CoNNL-U"
[Semiring Inc.]: https://semiring.com/ "Semiring Inc."
[Go JSON-NLP]: https://github.com/SemiringInc/GoJSONNLP "Go JSON-NLP"

# Python JSON-NLP Module

(C) 2019 by [Damir Cavar], [Oren Baldinger], Maanvitha Gongalla, Anurag Kumar, Murali Kammili

Brought to you by the [NLP-Lab.org]!


## Introduction


The Python [JSON-NLP] module contains general mapping functions for [JSON-NLP] to [CoNLL-U], a validator for the generated output, an Natural Language Processing (NLP) pipeline interface (for [Flair], [spaCy], [NLTK], [Polyglot], [Xrenner], etc.), and various utility functions.



## Installation

For more details, see [JSON-NLP].

This module is a wrapper for outputs from different NLP pipelines and modules into a standardized [JSON-NLP] format.

To install this package, run the following command:

    pip install pyjsonnlp

You might have to use *pip3* on some systems.

## Validation

[JSON-NLP] is based on a schema, built by [NLP-Lab.org], to comprehensively and concisely represent linguistic annotations. 
We provide a validator to help ensure that generated JSON validates against the schema:

    result = MyPipeline().proces(text="I am a sentence")
    assert pyjsonnlp.validation.is_valid(result)

## Conversion

To enable interoperability with other annotation formats, we support conversions between them.
Note that conversion could be lossy, if the relative depths of annotation are not the same.
Currently we have a [CoNLL-U] to [JSON-NLP] converter, that covers most annotations:

    pyjsonnlp.conversion.parse_conllu(conllu_text)
    
This functionality is still a work in progress.

## Pipeline

[JSON-NLP] provides a simple `Pipeline` interface that should be implemented for embedding into a microservice:
    
    from collections import OrderedDict

    class MockPipeline(pyjsonnlp.pipeline.Pipeline):
        @staticmethod
        def process(text='', coreferences=False, constituents=False, dependencies=False, expressions=False,
                    **kwargs) -> OrderedDict: 
            return OrderedDict()
            
The provided keyword arguments should be used to toggle on or off processing components within the method.        

## Microservice

The next step is the [JSON-NLP] a Microservice class, with a pre-built implementation of [Flask]. 

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


[Damir Cavar]: http://damir.cavar.me/ "Damir Cavar"
[Oren Baldinger]: https://oren.baldinger.me/ "Oren Baldinger"
[NLP-Lab.org]: http://nlp-lab.org/ "NLP-Lab.org"
[JSON-NLP]: https://github.com/dcavar/JSON-NLP "JSON-NLP"
[Flair]: https://github.com/zalandoresearch/flair "Flair"
[spaCy]: https://spacy.io/ "spaCy"
[NLTK]: http://nltk.org/ "Natural Language Processing Toolkit"
[Polyglot]: https://github.com/aboSamoor/polyglot "Polyglot" 
[Xrenner]: https://github.com/amir-zeldes/xrenner "Xrenner"
[CoNLL-U]: https://universaldependencies.org/format.html "CoNNL-U"

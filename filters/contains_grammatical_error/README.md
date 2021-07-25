## `contains_grammatical_error` filter

## What type of a filter is this?

This filter makes it easy to filter out those sentences in a specific language
which are grammatically correct, as evaluated by [LanguageTool](https://languagetool.org/).

Author: Marek Suppa

## Why is measuring performance on this split important?

Often times the NLP models end up being trained and evaluated on data that is
"unusually clean", in the sense that it expects all its training data to be
gramatically correct, which is often not the case in real-world scenarios.

This filter provides an easy way of finding parts of the input dataset that
would end up being marked as "not correct" by a spellchecker (and vice-versa),
allowing for better understanding of the performance of the model on this kind
of data.

## Related Work

## What are the limitations of this filter?

The filter depends on `language_tool_python`, which in turn depends on the
LanguageTool, which is effectively a 200MB .ZIP file that may end up being
troublesome to manage on some platforms.

LanguageTool also only supports the following languages:
- ar
- ast
- ast-ES
- be
- be-BY
- br
- br-FR
- ca
- ca-ES
- ca-ES-valencia
- da
- da-DK
- de
- de-AT
- de-CH
- de-DE
- de-DE-x-simple-language
- el
- el-GR
- en
- en-AU
- en-CA
- en-GB
- en-NZ
- en-US
- en-ZA
- eo
- es
- es-AR
- fa
- fr
- ga
- ga-IE
- gl
- gl-ES
- it
- ja
- ja-JP
- km
- km-KH
- nl
- nl-BE
- pl
- pl-PL
- pt
- pt-AO
- pt-BR
- pt-MZ
- pt-PT
- ro
- ro-RO
- ru
- ru-RU
- sk
- sk-SK
- sl
- sl-SI
- sv
- ta
- ta-IN
- tl
- tl-PH
- uk
- uk-UA
- zh
- zh-CN

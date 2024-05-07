from abc import ABCMeta as ABCMeta0
from builtins import str as str1
from typing import Union as Union2, Optional as Optional3, ClassVar as ClassVar4, Sequence as Sequence5
class RuleOption(metaclass = ABCMeta0):
  pass
class Rule(RuleOption):
  regex__20: 'str1'
  kind__21: 'TokenKind'
  state__22: 'Union2[str1, None]'
  __slots__ = ('regex__20', 'kind__21', 'state__22')
  def constructor__23(this__0, regex__24: 'str1', kind__25: 'TokenKind', state: Optional3['Union2[str1, None]'] = None) -> 'None':
    state__26: Optional3['Union2[str1, None]'] = state
    if state__26 is None:
      state__26 = None
    this__0.regex__20 = regex__24
    this__0.kind__21 = kind__25
    this__0.state__22 = state__26
  def __init__(this__0, regex__24: 'str1', kind__25: 'TokenKind', state: Optional3['Union2[str1, None]'] = None) -> None:
    state__26: Optional3['Union2[str1, None]'] = state
    this__0.constructor__23(regex__24, kind__25, state__26)
  @property
  def regex(this__68) -> 'str1':
    return this__68.regex__20
  @property
  def kind(this__72) -> 'TokenKind':
    return this__72.kind__21
  @property
  def state(this__76) -> 'Union2[str1, None]':
    return this__76.state__22
class TokenKind(metaclass = ABCMeta0):
  pass
class Default(RuleOption):
  state__27: 'str1'
  __slots__ = ('state__27',)
  def constructor__28(this__3, state__29: 'str1') -> 'None':
    this__3.state__27 = state__29
  def __init__(this__3, state__29: 'str1') -> None:
    this__3.constructor__28(state__29)
  @property
  def state(this__80) -> 'str1':
    return this__80.state__27
class Include(RuleOption):
  state__32: 'str1'
  __slots__ = ('state__32',)
  def constructor__33(this__6, state__34: 'str1') -> 'None':
    this__6.state__32 = state__34
  def __init__(this__6, state__34: 'str1') -> None:
    this__6.constructor__33(state__34)
  @property
  def state(this__84) -> 'str1':
    return this__84.state__32
class Inherit(RuleOption):
  __slots__ = ()
  def constructor__37(this__9) -> 'None':
    None
  def __init__(this__9) -> None:
    this__9.constructor__37()
class Kind(TokenKind):
  name__38: 'str1'
  comment_multiline: ClassVar4['Kind']
  comment_singleline: ClassVar4['Kind']
  keyword: ClassVar4['Kind']
  keyword_constant: ClassVar4['Kind']
  keyword_declaration: ClassVar4['Kind']
  name_kind: ClassVar4['Kind']
  name_builtin: ClassVar4['Kind']
  name_decorator: ClassVar4['Kind']
  number: ClassVar4['Kind']
  operator: ClassVar4['Kind']
  punctuation: ClassVar4['Kind']
  string_plain: ClassVar4['Kind']
  string_regex: ClassVar4['Kind']
  string_interpol: ClassVar4['Kind']
  whitespace: ClassVar4['Kind']
  __slots__ = ('name__38',)
  def constructor__54(this__11, name__55: 'str1') -> 'None':
    this__11.name__38 = name__55
  def __init__(this__11, name__55: 'str1') -> None:
    this__11.constructor__54(name__55)
  @property
  def name(this__87) -> 'str1':
    return this__87.name__38
Kind.comment_multiline = Kind('Comment.Multiline')
Kind.comment_singleline = Kind('Comment.Singleline')
Kind.keyword = Kind('Keyword')
Kind.keyword_constant = Kind('Keyword.Constant')
Kind.keyword_declaration = Kind('Keyword.Declaration')
Kind.name_kind = Kind('Name')
Kind.name_builtin = Kind('Name.Builtin')
Kind.name_decorator = Kind('Name.Decorator')
Kind.number = Kind('Number')
Kind.operator = Kind('Operator')
Kind.punctuation = Kind('Punctuation')
Kind.string_plain = Kind('String')
Kind.string_regex = Kind('String.Regex')
Kind.string_interpol = Kind('String.Interpol')
Kind.whitespace = Kind('Whitespace')
class ByGroups(TokenKind):
  kinds__56: 'Sequence5[TokenKind]'
  __slots__ = ('kinds__56',)
  def constructor__57(this__13, kinds__58: 'Sequence5[TokenKind]') -> 'None':
    this__13.kinds__56 = kinds__58
  def __init__(this__13, kinds__58: 'Sequence5[TokenKind]') -> None:
    this__13.constructor__57(kinds__58)
  @property
  def kinds(this__91) -> 'Sequence5[TokenKind]':
    return this__91.kinds__56
class Using(TokenKind):
  lexer__61: 'str1'
  __slots__ = ('lexer__61',)
  def constructor__62(this__17, lexer__63: 'str1') -> 'None':
    this__17.lexer__61 = lexer__63
  def __init__(this__17, lexer__63: 'str1') -> None:
    this__17.constructor__62(lexer__63)
  @property
  def lexer(this__95) -> 'str1':
    return this__95.lexer__61
def default(state__30: 'str1') -> 'Default':
  return Default(state__30)
def include(state__35: 'str1') -> 'Include':
  return Include(state__35)
inherit: 'Inherit' = Inherit()
def bygroups(kinds__59: 'Sequence5[TokenKind]') -> 'ByGroups':
  return ByGroups(kinds__59)
def using(lexer__64: 'str1') -> 'Using':
  return Using(lexer__64)

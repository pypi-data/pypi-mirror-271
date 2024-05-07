from temper_syntax.pygments import RuleOption as RuleOption__15, Include as Include__20, Default as Default__18, Inherit as Inherit__22, ByGroups as ByGroups__24, Using as Using__26, include as include__21, Rule as Rule__16, Kind as Kind__23, default as default__19, TokenKind as TokenKind__17, bygroups as bygroups__25, using as using__27, inherit as inherit__28
from builtins import str as str1, tuple as tuple7
from typing import Sequence as Sequence5, Optional as Optional3
from types import MappingProxyType as MappingProxyType6
from temper_core import Pair as Pair_357, cast_by_type as cast_by_type8, map_constructor as map_constructor_358, str_cat as str_cat_359, list_join as list_join_360
class TemperLexer:
  name__29: 'str1'
  aliases__30: 'Sequence5[str1]'
  filenames__31: 'Sequence5[str1]'
  tokens__32: 'MappingProxyType6[str1, (Sequence5[RuleOption__15])]'
  __slots__ = ('name__29', 'aliases__30', 'filenames__31', 'tokens__32')
  def constructor__33(this__0, name: Optional3['str1'] = None, aliases: Optional3['Sequence5[str1]'] = None, filenames: Optional3['Sequence5[str1]'] = None, tokens: Optional3['MappingProxyType6[str1, (Sequence5[RuleOption__15])]'] = None) -> 'None':
    name__34: Optional3['str1'] = name
    aliases__35: Optional3['Sequence5[str1]'] = aliases
    filenames__36: Optional3['Sequence5[str1]'] = filenames
    tokens__37: Optional3['MappingProxyType6[str1, (Sequence5[RuleOption__15])]'] = tokens
    t_314: 'MappingProxyType6[str1, (Sequence5[RuleOption__15])]'
    t_316: 'Pair_357[str1, (Sequence5[RuleOption__15])]'
    t_319: 'Pair_357[str1, (Sequence5[RuleOption__15])]'
    t_324: 'Pair_357[str1, (Sequence5[RuleOption__15])]'
    t_328: 'Pair_357[str1, (Sequence5[RuleOption__15])]'
    t_197: 'Sequence5[RuleOption__15]'
    t_202: 'Sequence5[RuleOption__15]'
    t_208: 'Sequence5[RuleOption__15]'
    t_212: 'Sequence5[RuleOption__15]'
    t_215: 'Sequence5[RuleOption__15]'
    if name__34 is None:
      name__34 = 'Temper'
    if aliases__35 is None:
      aliases__35 = ('temper',)
    if filenames__36 is None:
      filenames__36 = ('*.temper',)
    if tokens__37 is None:
      t_197 = cast_by_type8((include__21('commentsandwhitespace'), Rule__16(words__13('false', 'NaN', 'null', 'true', 'void'), Kind__23.keyword_constant), Rule__16(words__13('class', 'interface', 'let', 'private', 'public', 'sealed', 'var'), Kind__23.keyword_declaration), Rule__16(words__13('do', 'else', 'export', 'extends', 'fn', 'if', 'import', 'is', 'match', 'new', 'orelse'), Kind__23.keyword), Rule__16(words__13('return', 'yield'), Kind__23.keyword, 'slashstartsregex'), Rule__16(words__13('AnyValue', 'Boolean', 'Float64', 'Function', 'Int', 'List', 'ListBuilder', 'Listed', 'Map', 'MapBuilder', 'MapKey', 'Mapped', 'NoResult', 'Null', 'String', 'StringSlice', 'Void'), Kind__23.name_builtin), Rule__16('(?<=\\brgx)"', Kind__23.string_regex, 'stringregex'), Rule__16('"', Kind__23.string_plain, 'string'), Rule__16('[-=+*&|<>]+|/=?', Kind__23.operator, 'slashstartsregex'), Rule__16('[{}();:.,]', Kind__23.punctuation, 'slashstartsregex'), Rule__16('\\d+\\.?\\d*|\\.\\d+', Kind__23.number), Rule__16('@[_<<Lu>><<Ll>>][_<<Lu>><<Ll>>0-9]*', Kind__23.name_decorator), Rule__16('[_<<Lu>><<Ll>>][_<<Lu>><<Ll>>0-9]*', Kind__23.name_kind)), tuple7)
      t_328 = Pair_357('root', t_197)
      t_202 = cast_by_type8((Rule__16('\\s+', Kind__23.whitespace), Rule__16('//.*?$', Kind__23.comment_singleline), Rule__16('/\\*', Kind__23.comment_multiline, 'nestedcomment')), tuple7)
      t_324 = Pair_357('commentsandwhitespace', t_202)
      t_208 = cast_by_type8((Rule__16('[^*/]+', Kind__23.comment_multiline), Rule__16('/\\*', Kind__23.comment_multiline, '#push'), Rule__16('\\*/', Kind__23.comment_multiline, '#pop'), Rule__16('[*/]', Kind__23.comment_multiline)), tuple7)
      t_319 = Pair_357('nestedcomment', t_208)
      t_212 = cast_by_type8((include__21('commentsandwhitespace'), Rule__16('/(\\\\.|[^[/\\\\\\n]|\\[(\\\\.|[^\\]\\\\\\n])*])+/([gimuysd]+\\b|\\B)', Kind__23.string_regex, '#pop'), default__19('#pop')), tuple7)
      t_316 = Pair_357('slashstartsregex', t_212)
      t_215 = cast_by_type8((Rule__16('}', Kind__23.string_interpol, '#pop'), include__21('root')), tuple7)
      t_314 = map_constructor_358((t_328, t_324, t_319, t_316, Pair_357('interpolation', t_215), stringish__12('string', Kind__23.string_plain), stringish__12('stringregex', Kind__23.string_regex)))
      tokens__37 = t_314
    this__0.name__29 = name__34
    this__0.aliases__30 = aliases__35
    this__0.filenames__31 = filenames__36
    this__0.tokens__32 = tokens__37
  def __init__(this__0, name: Optional3['str1'] = None, aliases: Optional3['Sequence5[str1]'] = None, filenames: Optional3['Sequence5[str1]'] = None, tokens: Optional3['MappingProxyType6[str1, (Sequence5[RuleOption__15])]'] = None) -> None:
    name__34: Optional3['str1'] = name
    aliases__35: Optional3['Sequence5[str1]'] = aliases
    filenames__36: Optional3['Sequence5[str1]'] = filenames
    tokens__37: Optional3['MappingProxyType6[str1, (Sequence5[RuleOption__15])]'] = tokens
    this__0.constructor__33(name__34, aliases__35, filenames__36, tokens__37)
  @property
  def name(this__55) -> 'str1':
    return this__55.name__29
  @property
  def aliases(this__59) -> 'Sequence5[str1]':
    return this__59.aliases__30
  @property
  def filenames(this__63) -> 'Sequence5[str1]':
    return this__63.filenames__31
  @property
  def tokens(this__67) -> 'MappingProxyType6[str1, (Sequence5[RuleOption__15])]':
    return this__67.tokens__32
class TemperMdLexer:
  name__44: 'str1'
  aliases__45: 'Sequence5[str1]'
  filenames__46: 'Sequence5[str1]'
  tokens__47: 'MappingProxyType6[str1, (Sequence5[RuleOption__15])]'
  __slots__ = ('name__44', 'aliases__45', 'filenames__46', 'tokens__47')
  def constructor__48(this__7, name: Optional3['str1'] = None, aliases: Optional3['Sequence5[str1]'] = None, filenames: Optional3['Sequence5[str1]'] = None, tokens: Optional3['MappingProxyType6[str1, (Sequence5[RuleOption__15])]'] = None) -> 'None':
    name__49: Optional3['str1'] = name
    aliases__50: Optional3['Sequence5[str1]'] = aliases
    filenames__51: Optional3['Sequence5[str1]'] = filenames
    tokens__52: Optional3['MappingProxyType6[str1, (Sequence5[RuleOption__15])]'] = tokens
    t_300: 'MappingProxyType6[str1, (Sequence5[RuleOption__15])]'
    t_302: 'Pair_357[str1, (Sequence5[RuleOption__15])]'
    t_162: 'Sequence5[RuleOption__15]'
    t_165: 'Sequence5[RuleOption__15]'
    if name__49 is None:
      name__49 = 'TemperMarkdown'
    if aliases__50 is None:
      aliases__50 = ('temper.md', 'tempermd')
    if filenames__51 is None:
      filenames__51 = ('*.temper.md', '*.tempermd')
    if tokens__52 is None:
      t_162 = cast_by_type8((Rule__16('^\\s*\\n {4}', Kind__23.whitespace, 'indented'), inherit__28), tuple7)
      t_302 = Pair_357('root', t_162)
      t_165 = cast_by_type8((Rule__16('(?s)(.*?)(?=\\Z|\\n(?: {1,3}[^ ]|[^ ]|$))', bygroups__25((using__27('Temper'),)), '#pop'),), tuple7)
      t_300 = map_constructor_358((t_302, Pair_357('indented', t_165)))
      tokens__52 = t_300
    this__7.name__44 = name__49
    this__7.aliases__45 = aliases__50
    this__7.filenames__46 = filenames__51
    this__7.tokens__47 = tokens__52
  def __init__(this__7, name: Optional3['str1'] = None, aliases: Optional3['Sequence5[str1]'] = None, filenames: Optional3['Sequence5[str1]'] = None, tokens: Optional3['MappingProxyType6[str1, (Sequence5[RuleOption__15])]'] = None) -> None:
    name__49: Optional3['str1'] = name
    aliases__50: Optional3['Sequence5[str1]'] = aliases
    filenames__51: Optional3['Sequence5[str1]'] = filenames
    tokens__52: Optional3['MappingProxyType6[str1, (Sequence5[RuleOption__15])]'] = tokens
    this__7.constructor__48(name__49, aliases__50, filenames__51, tokens__52)
  @property
  def name(this__71) -> 'str1':
    return this__71.name__44
  @property
  def aliases(this__75) -> 'Sequence5[str1]':
    return this__75.aliases__45
  @property
  def filenames(this__79) -> 'Sequence5[str1]':
    return this__79.filenames__46
  @property
  def tokens(this__83) -> 'MappingProxyType6[str1, (Sequence5[RuleOption__15])]':
    return this__83.tokens__47
def words__13(*names__41: 'str1') -> 'str1':
  global list_join_360, str_cat_359
  def fn__353(x__43: 'str1') -> 'str1':
    return x__43
  return str_cat_359('\\b(?:', list_join_360(names__41, '|', fn__353), ')\\b')
def stringish__12(key__38: 'str1', kind__39: 'TokenKind__17') -> 'Pair_357[str1, (Sequence5[RuleOption__15])]':
  global Pair_357
  t_223: 'Sequence5[RuleOption__15]'
  t_223 = cast_by_type8((Rule__16('"', kind__39, '#pop'), Rule__16('\\$\\{', Kind__23.string_interpol, 'interpolation'), Rule__16('(?:[^"$]|\\$[^{])+', kind__39)), tuple7)
  return Pair_357(key__38, t_223)

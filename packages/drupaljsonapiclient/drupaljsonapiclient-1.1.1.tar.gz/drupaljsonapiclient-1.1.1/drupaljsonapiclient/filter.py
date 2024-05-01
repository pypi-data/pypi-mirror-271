from typing import TYPE_CHECKING, Union, Dict, Sequence

if TYPE_CHECKING:
    FilterKeywords = Dict[str, Union[str, Sequence[Union[str, int, float]]]]
    IncludeKeywords = Sequence[str]


class Modifier:
    """
    Base class for query modifiers.
    You can derive your own class and use it if you have custom syntax.
    """
    def __init__(self, query_str: str='') -> None:
        self._query_str = query_str

    def url_with_modifiers(self, base_url: str) -> str:
        """
        Returns url with modifiers appended.

        Example:
            Modifier('filter[attr1]=1,2&filter[attr2]=2').filtered_url('doc')
              -> 'GET doc?filter[attr1]=1,2&filter[attr2]=2'
        """
        filter_query = self.appended_query()
        fetch_url = f'{base_url}?{filter_query}'
        return fetch_url

    def appended_query(self) -> str:
        return self._query_str

    def __add__(self, other: 'Modifier') -> 'Modifier':
        mods = []
        for m in [self, other]:
            if isinstance(m, ModifierSum):
                mods += m.modifiers
            else:
                mods.append(m)
        return ModifierSum(mods)


class ModifierSum(Modifier):
    def __init__(self, modifiers):
        self.modifiers = modifiers

    def appended_query(self) -> str:
        return '&'.join(m.appended_query() for m in self.modifiers)


class Filter(Modifier):
    """
    Implements query filtering for Session.get etc.
    You can derive your own filter class and use it if you have a
    custom filter query syntax.
    """
    def __init__(self, query_str: str='', **filter_kwargs: 'FilterKeywords') -> None:
        """
        :param query_str: Specify query string manually.
        :param filter_kwargs: Specify required conditions on result.
            Example: Filter(attribute='1', relation__attribute='2')
        """
        super().__init__(query_str)
        self._filter_kwargs = filter_kwargs

    # This and next method prevent any existing subclasses from breaking
    def url_with_modifiers(self, base_url: str) -> str:
        return self.filtered_url(base_url)

    def filtered_url(self, base_url: str) -> str:
        return super().url_with_modifiers(base_url)

    def appended_query(self) -> str:
        return super().appended_query() or self.format_filter_query(**self._filter_kwargs)

    def format_filter_query(self, **kwargs: 'FilterKeywords') -> str:
        """
        Filter class that implements url filtering scheme according to JSONAPI
        recommendations (http://jsonapi.org/recommendations/)
        """
        def jsonify_key(key):
            return key.replace('__', '.').replace('_', '-')
        return '&'.join(f'filter[{jsonify_key(key)}]={value}'
                        for key, value in kwargs.items())


class Inclusion(Modifier):
    """
    Implements query inclusion for Session.get etc.
    """
    def __init__(self, *include_args: 'IncludeKeywords') -> None:
        super().__init__()
        self._include_args = include_args

    def appended_query(self) -> str:
        includes = ','.join(self._include_args)
        return f'include={includes}'

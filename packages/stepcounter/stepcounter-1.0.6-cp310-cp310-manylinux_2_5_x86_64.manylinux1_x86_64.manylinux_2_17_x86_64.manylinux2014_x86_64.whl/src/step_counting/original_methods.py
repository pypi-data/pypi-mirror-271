import builtins

########################################################################################
# In parts of code that run with patches applied we need to use that have not been
# patched. For that reason we keep these methods so we can use their unchanged
# functionality later in the code.
########################################################################################

_hash = hash
_setattr = setattr
_callable = callable

_import = builtins.__import__

dict_get = dict.get
list_append = list.append

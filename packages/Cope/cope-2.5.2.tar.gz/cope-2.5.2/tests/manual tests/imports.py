from Cope.imports import lazy_import

#%% Test lazy_import
print('a')
package = lazy_import('this')
print('b')
if package:
    print('imported!')
else:
    print('not imported.')
print('b.5')
print(package)
print('c')
print(package.d)
print('d')

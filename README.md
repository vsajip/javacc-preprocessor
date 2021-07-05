This preprocessor is based on [JavaCC's 
preprocessor](https://github.com/javacc21/javacc21/tree/master/examples/preprocessor). 
Whereas that is based on strict adherence to C#'s preprocessor (symbols 
are Boolean values only), this version expands the functionality so 
that you could add symbols with string values, perhaps by passing 
-D<sym>=<value>. Only simple identifiers are supported as values (e.g. 
no spaces or punctuation) in order to support constructs like `#if 
CODELANG == python` in preprocessed files. This is to potentially 
facilitate support for multiple code generation languages in JavaCC:

```
# if CODELANG == python
Some Python code here
#elif CODELANG == csharp
Some C# code here
#else
Some Java code here
#endif
```

This code is a proof of concept; more work may be needed, and more 
tests are definitely needed. Jython is used for (JUnit-style) tests, so 
you may want to [download it](https://www.jython.org/download) if you 
want to run the tests. I use the standalone Jython jar and a simple
shell script:

```
#!/usr/bin/sh
java -jar $HOME/.local/bin/jython.jar $*
```

Jython is used  as it's quicker (for me -- YMMV) to write tests than in 
Java.


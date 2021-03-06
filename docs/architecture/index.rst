Architecture
############

This project has been constructed following the guidelines of the
Clean Architecture by Uncle Bob as exposed in: 
https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html.

There are basically two structural namespaces inside of the
*'authark'* package which are *'app'* and *'infra'*. In essence, nothing
inside **'app'** can refer to something outside it and should use abstractions
and dependency inversion patterns to represent such dependencies.

The **'infra'** package provides concrete implementations of the interfaces
exposed in the application and logical layer (i.e. **'app'** package), keeping
the latter technology agnostic and improving its testability.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   domain.rst
   layout.rst
   protocol.rst

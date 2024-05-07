Title using `-`
---------------

Title using `*`
***************

Title using `=`
===============

Title using `%%`
~~~~~~~~~~~~~~~~

.. ipython:: python

        print("A simple code block")
        
        # with a comment
        
.. code-example:: A code block

    .. ipython:: python

        
        print("A code block")
        
.. code-example:: A collapsible code block
    :collapsible:

    .. ipython:: python

        
        print("A code block")
        
.. code-example:: A collapsible (open) code block
    :collapsible: open

    .. ipython:: python

        
        print("A code block")
        
        
.. md-tab-set::    :class: custom-tab-set-style

    .. md-tab-item:: tab_1

        .. ipython:: python

                [i for i in range(5)]
        
                # a comment
        
        Some text

    .. md-tab-item:: tab 2

        This is how to include text.

.. ipython:: python

        print("Be careful. If this is followed by <> it does not get included")
        # todo: maybe it needs to get fixed
        
.. md-tab-set::    :class: custom-tab-set-style

    .. md-tab-item:: example

        .. ipython:: python

                "ABS"
        
.. code-example:: Imports

    .. ipython:: python

        
        import json
        
New Title
~~~~~~~~~

.. ipython:: python

        print("If you include a separator, like some text")
        


.. code-example:: Imports

    .. ipython:: python

        
        import json
        
using
~~~~~

.. ipython:: python

        # example code
        
        import itertools
        
Now a plot

using matplotlib
~~~~~~~~~~~~~~~~

.. ipython:: python

        print("ciao!")
        
check
*****

.. ipython:: python

        print("ciao!")

.. _flowchart:

Workflow
================

The tool was written following a proposal not only to retrieve data from archived tweets, but also to facilitate the reading of these tweets. Therefore, a flow is defined to obtain these results in the best possible way.

Due to limitations of the Wayback CDX Server API, it is not always possible to parse the results with the mimetype ``application/json``, regardless, the data in CDX format are saved.

Use the mouse to zoom in and out the flowchart.

.. mermaid::
   :zoom:
   :align: center

   flowchart TB
      A[input Username]--> B[(Wayback Machine)]
      B--> B1[save Archived Tweets CDX data]
      B1--> |parsing| C{embed Tweet URL\nvia Twitter Publisher}
      C--> |2xx/3xx| D[return Tweet text]
      C--> |4xx| E[return None]
      E--> F{request Archived\nTweet URL}
      F--> |4xx| G[return Only CDX data]
      F--> |TODO: 2xx/3xx: application/json| J[return JSON text]
      F--> |2xx/3xx: text/html, warc/revisit, unk| K[return HTML iframe tag]

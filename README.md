# Mining MOOSE GitHub discussion

The MOOSE GitHub discussion forum (https://github.com/idaholab/moose/discussions) has been running for a few years. Users from across the world have asked questions on the forum. The vast majority of questions have been answered. For those without an accepted answer, some useful discussion has taken place.

These questions and answers serve as a valuable knowledge base for the MOOSE community.

This repository provides some experimental routines to help construct and mine such knowledge base.

## Example

In particular, the example given here showcases how a transformer can "pre-review" a new question and list the most similar posts.

Such task can be decomposed into the following steps:
1. `fetch.py`: Fetch all existing questions and answers from the GitHub discussion forum.
2. `build_db.py`: Post-process the fetched data and build a database of content encodings.
3. `recommend.py`: Encode the new question(s) and make suggestions, i.e., find the most similar posts from the database.

### `fetch.py`

This script demonstrates how one can programmatically fetch relevant information from the GitHub discussion forum. It uses GraphQL to form the query.

An environment variable named `GITHUB_TOKEN` should exist while running the script. The token should be granted sufficient access to read the repository.

The script automatically traverses through pagination to fetch information from each discussion post until either all posts have been fetched or no available credit remains.

Each page is stored in JSON format, including multiple posts; each post contains the original question (key "bodyText") and zero or more comments (key "comments"); each comment may have zero or more replies (key "replies").

### `build_db.py`

This script uses a transformer (in this example a simple "all-MiniLM-L6-v2" transformer) to encode fetched posts. The content of each post is assumed to be the concatenation of the body text of the question, the body text of each comment, and the body text of each reply.

The content is encoded by the transformer into a sentence embedding. The embeddings of all posts are written to the disk upon completion, along with a metadata file "meta.csv" including the title and URL of all posts.

### `recommend.py`

The heavy-lifting has been done in the previous scripts. The idea is that a lot of work can be done off-line (i.e., to build the database), and it becomes relatively cheap to make suggestions.

This script uses the same sentence transformer to encode the new question(s) and calculates their cosine similarity between existing posts. The 5 most similar posts are collected from the database.

An example output of the script is shown below:

```
-------------------------------------------------------------------------------
Question: How do I make my code more efficient?
    1. Title: Simulation stuck on really small time steps
        URL: https://github.com/idaholab/moose/discussions/26439
        Similarity: 0.4467
    2. Title: simulations running very slow
        URL: https://github.com/idaholab/moose/discussions/28612
        Similarity: 0.3988
    3. Title: Slower when computing across nodes
        URL: https://github.com/idaholab/moose/discussions/19598
        Similarity: 0.3929
    4. Title: how to  improve the efficiency of HPC process?
        URL: https://github.com/idaholab/moose/discussions/29088
        Similarity: 0.3808
    5. Title: Ways to reduce the calculation time
        URL: https://github.com/idaholab/moose/discussions/16483
        Similarity: 0.3800
-------------------------------------------------------------------------------
Question: Why is my simulation not converging?
    1. Title: Why can't my simulation converge
        URL: https://github.com/idaholab/moose/discussions/24512
        Similarity: 0.6064
    2. Title: Restart simulation does not converge while single simulation does
        URL: https://github.com/idaholab/moose/discussions/24979
        Similarity: 0.6048
    3. Title: Why can't my simulation converge?
        URL: https://github.com/idaholab/moose/discussions/21826
        Similarity: 0.5935
    4. Title: "solve did not converge" problem
        URL: https://github.com/idaholab/moose/discussions/22137
        Similarity: 0.5909
    5. Title: Convergence problem (maybe the Jacobian issue?)
        URL: https://github.com/idaholab/moose/discussions/24535
        Similarity: 0.5542
-------------------------------------------------------------------------------
Question: How to set up a fluid-structure interaction problem?
    1. Title: How to mix fluids in the TH Module Single-Phase-Flow tutorial?
        URL: https://github.com/idaholab/moose/discussions/23132
        Similarity: 0.5461
    2. Title: Use PorousFlowOutflowBC outside of Porous Flow module architecture
        URL: https://github.com/idaholab/moose/discussions/20590
        Similarity: 0.5325
    3. Title: nodal - FV variable coupling
        URL: https://github.com/idaholab/moose/discussions/23494
        Similarity: 0.5317
    4. Title: Nested Mesh Interaction
        URL: https://github.com/idaholab/moose/discussions/18267
        Similarity: 0.5230
    5. Title: Navier-Stokes Set-up
        URL: https://github.com/idaholab/moose/discussions/17017
        Similarity: 0.5194
-------------------------------------------------------------------------------
```

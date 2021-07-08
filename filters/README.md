## What is a filter?
Just the way transformations can transform examples of text, filters can identify whether an example follows some pattern of text! The only difference is that while transformations return another example of the same input format, filters return True or False!

### The List of Filters

This directory contains filters that are used to create contrast sets. A list of data points are fed through the filter to match the condition (e.g. the input text length should be above certain threshold, the input text should contain some keywords, etc.). Each subdirectory contains a single filter to construct contrast sets. A summary table of these filters follows.

The following describes the list of filters or conditions which split the dataset into contrast sets.

| Filter                             | Description                                                                       
| ------- | -----------                          
| [TextContainsKeywordsFilter](keywords)              | Selects examples which contain a pre-defined set of keywords.                
| [TextLengthFilter](length)     | Selects sentences/paragraphs of a specified length.


### How to Add a New Filter
Note that the instructions below are exactly the same as that of adding a new transformation except that new filters should be created in the the filters folder (current one).
### Setup

First, [fork the repository](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo) in GitHub! :fork_and_knife:
<a href="https://docs.github.com/en/github/getting-started-with-github/fork-a-repo">
<div style="text-align:center"><img src="https://docs.github.com/assets/images/help/repository/fork_button.jpg" alt="fork button" width="500"/></div>
</a>

Your fork will have its own location, which we will call `PATH_TO_YOUR_FORK`.
Next, [clone the forked repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) and create a branch for your filter, which here we will call **my_awesome_filter**:
```bash
git clone $PATH_TO_YOUR_FORK
cd NL-Augmenter
git checkout -b my_awesome_filter
```
We will base our filter on an existing example.
Create a new filter directory by copying over an existing filter `keywords`:
```bash
cd filters/
cp -r keywords my_awesome_filter
cd my_awesome_filter
```

### Creating a filter
1. Rename `keywords.py` to `my_awesome_filter.py` and choose one of the interfaces from the `interfaces/` folder. See the full list of options [here.](../interfaces)
2. Now put all your creativity in implementing the `filter` method. If you intend to use external libraries, add them with their version numbers in [`requirements.txt`](../requirements.txt)
3. Once done add at least 5 example pairs as test cases in the file `test.json` so that no one breaks your code inadvertently and update `my_awesome_filter/README.md`.


**Testing and evaluating**

Once the filter is ready, test it:
```bash
pytest -s --f=my_awesome_filter
```

**Code Styling** To standardized the code we use the [black](https://github.com/psf/black) code formatter which will run at the time of pre-commit.
To use pre-commit hook, install `pre-commit` with `pip install pre-commit` (installed by default if you've followed the above instructions). 
Then run `pre-commit install` to install the hook. On future commits, you should see the black code formatter is run on all python files you've staged for commit.

### Submitting

Once the tests pass and you are happy with the transformation, submit your transformation for review.
First, commit and push your changes:
```bash
git add filters/my_awesome_filter/*
git commit -m "Added my_awesome_filter"
git push --set-upstream origin my_awesome_filter
```
Finally, [submit a pull request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).
The last `git push` command prints a URL that can be copied into a browser to initiate such a pull request.
Alternatively, you can do so from the GitHub website.
<a href="https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request">
<div style="text-align:center"><img src="https://docs.github.com/assets/images/help/pull_requests/pull-request-start-review-button.png" alt="pull request button" width="500"/></div>
</a>

:sparkles: Congratulations, you've submitted a filter to NL-Augmenter! :sparkles:
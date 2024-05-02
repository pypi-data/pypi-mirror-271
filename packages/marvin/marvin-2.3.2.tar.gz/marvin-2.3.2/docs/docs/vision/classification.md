# Classifying images

Marvin can use OpenAI's vision API to process images and classify them into categories.

The `marvin.beta.classify` function is an enhanced version of `marvin.classify` that accepts images as well as text. 

!!! tip "Beta"
    Please note that vision support in Marvin is still in beta, as OpenAI has not finalized the vision API yet. While it works as expected, it is subject to change.

<div class="admonition abstract">
  <p class="admonition-title">What it does</p>
  <p>
    The <code>classify</code> function can classify images as one of many labels.
  </p>
</div>


<div class="admonition info">
  <p class="admonition-title">How it works</p>
  <p>
    
  This involves a two-step process: first, a caption is generated for the image that is aligned with the structuring goal. Next, the actual classify operation is performed with an LLM.

  </p>
</div>



!!! example "Example"

    We will classify the animal in this image, as well as whether it is wet or dry:

    ![](https://upload.wikimedia.org/wikipedia/commons/d/d5/Retriever_in_water.jpg)

    
    ```python
    import marvin

    img = marvin.beta.Image('https://upload.wikimedia.org/wikipedia/commons/d/d5/Retriever_in_water.jpg')

    animal = marvin.beta.classify(
        img, 
        labels=['dog', 'cat', 'bird', 'fish', 'deer']
    )
    
    dry_or_wet = marvin.beta.classify(
        img, 
        labels=['dry', 'wet'], 
        instructions='Is the animal wet?'
    )
    ```

    !!! success "Result"
        ```python
        assert animal == 'dog'
        assert dry_or_wet == 'wet'
        ```




## Model parameters
You can pass parameters to the underlying API via the `model_kwargs` and `vision_model_kwargs` arguments of `classify`. These parameters are passed directly to the respective APIs, so you can use any supported parameter.


## Async support

If you are using Marvin in an async environment, you can use `classify_async`:

```python
result = await marvin.beta.classify_async(
    "The app crashes when I try to upload a file.", 
    labels=["bug", "feature request", "inquiry"]
) 

assert result == "bug"
```

## Mapping

To classify a list of inputs at once, use `.map`:

```python
inputs = [
    "The app crashes when I try to upload a file.",
    "How do change my password?"
]
result = marvin.beta.classify.map(inputs, ["bug", "feature request", "inquiry"])
assert result == ["bug", "inquiry"]
```

(`marvin.beta.classify_async.map` is also available for async environments.)

Mapping automatically issues parallel requests to the API, making it a highly efficient way to classify multiple inputs at once. The result is a list of classifications in the same order as the inputs.
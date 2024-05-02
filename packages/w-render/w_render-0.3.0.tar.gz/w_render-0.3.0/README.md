### Description

Web-render is a method of rendering dynamic web pages using Selenium.


#### Example

_Любой из элементов на странице_

```python
render.set_url("https://site.com", web_wait={
        "name": "CheckElementInDOM",
        "params": {
            "css_selectors": ["#a-1", "#a-2"],
        }
    }
)
```

_Указанные элементы на странице_

```python
render.set_url("https://site.com", web_wait={
        "name": "CheckElementsInDOM",
        "params": {
            "css_selectors": ["#a-1", "#a-2"],
        }
    }
)
```

_Количество элементов на странице больше или равно count_

```python
render.set_url("https://site.com", web_wait={
        "name": "CheckNumberElementsInPage",
        "params": {
            "selector":"[data-widget=searchResultsV2] a.tile-hover-target[data-prerender]",
            "count": 30
        }
    }
)
```
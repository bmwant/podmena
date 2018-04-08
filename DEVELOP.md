### Releasing

```
$ git tag -a v0.4.1 -m "tagging 0.4.1" 
$ git push --tags
$ python setup.py sdist
$ twine upload
```

### TODO

* Command to display current status
* Show update diff/total number of emoji

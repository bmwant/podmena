## podmena

Enhance your commit messages with emoji :cherries:

podmena will automatically add random emoji to every commit message for any
git repository installed.

![emoji](https://github.com/bmwant/podmena/blob/master/podmena.png)

873 items in database so far!

Credits go to [WebpageFX](https://www.webpagefx.com/tools/emoji-cheat-sheet/) 
for list of emoji!

### Installation

```bash
$ pip install podmena
```
Activate for current git repository
```bash
$ podmena add local
```
Activate globally for all repositories (works with git `2.9.1` and above)
```bash
$ git --version
$ podmena add global
```
Deactivate it
```bash
$ podmena rm local
$ podmena rm global
```
Check current status if you not sure
```bash
$ podmena status
```
And finally `podmena --version` and `podmena --help` in case you need more 
details.


Note that uninstalling globally will not remove hooks from repositories where
it was installed locally. You need to switch to that directory and uninstall it
locally as well.

### See also

* [GitHooks](https://githooks.com/)
* [Atlassian tutorial for git hooks](https://www.atlassian.com/git/tutorials/git-hooks)
Thanks [@kakovskyi](https://github.com/kakovskyi) working for Atlassian!
* It's a wrong place to search if you are looking for lemonparty :lemon: club

### Say thanks!

Visit [this page](https://gimmebackmyson.herokuapp.com/) 
and donate some money if you enjoy this _crazy_ project!

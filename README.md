## podmena

![Checks](https://github.com/bmwant/podmena/actions/workflows/tests.yml/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Enhance your commit messages with emoji 🍒

podmena will automatically add random emoji to every commit message for any
git repository installed.

![emoji](https://github.com/bmwant/podmena/blob/main/podmena.png)

873 items in database so far!

Credits go to [WebpageFX](https://www.webpagefx.com/tools/emoji-cheat-sheet/)
for list of emoji!

### Installation

```bash
$ pip install podmena
```

* Activate for current git repository

```bash
$ podmena add local
```

You can also replace `add` with a different alias

`activate` / `enable` / `install` / `on`

e.g. `podmena enable local`

* Activate globally for all repositories (works with git `2.9.1` and above)

```bash
$ git --version
$ podmena add global  # Aliases work here as well
```

* Deactivate it
```bash
$ podmena rm local
$ podmena rm global
```

You can replace `rm` with any of these available aliases

`remove` / `delete` / `deactivate` / `disable` / `off` / `uninstall`

e.g. `podmena deactivate local`

* Check current status if you not sure

```bash
$ podmena status
```

* And finally `podmena --version` and `podmena --help` in case you need more
details.

> **NOTE:** uninstalling globally will not remove hooks from repositories where
it was installed locally. You need to switch to that directory manually and uninstall it locally as well.

### Contribute

See [DEVELOP.md](https://github.com/bmwant/podmena/blob/main/DEVELOP.md) to setup your local development environment and feel free to create a pull request with a new feature.

### Releases

See [CHANGELOG.md](https://github.com/bmwant/podmena/blob/main/CHANGELOG.md) for the new features included within each release.

### See also

* [GitHooks](https://githooks.com/)
* [Atlassian tutorial for git hooks](https://www.atlassian.com/git/tutorials/git-hooks)
Thanks [@kakovskyi](https://github.com/kakovskyi) working for Atlassian!
* It's a wrong place to search if you are looking for 🍋 lemonparty.fun 🍋 club

### Say thanks!

🐶 `D7DA74qzZUyh9cctCxWovPTEovUSjGzL2S` this is [Dogecoin](https://dogecoin.com/) wallet to support the project.

# poetry-stabs-package-sample

パッケージ公開サンプル

```
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry publish -r poetry-stabs-package-sample
```

# 型を付ける

# テストを書く

# awesome linters

# documents

# publish package

pypa/gh-action-pypi-publish@release/v1 を使うと公開できる、pypi とは odic で連携してるっぽいので事前に pypi の設定が必要
https://docs.github.com/ja/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-pypi

## poetry publish をする

poetry に token の設定が必要

普通に公開しようとすると夏期のようなエラーが出た

```
❯ poetry publish --build -r testpypi
There are 2 files ready for publishing. Build anyway? (yes/no) [no] yes
Building poetry-stabs-package-sample (0.1.0)
  - Building sdist
  - Built poetry_stabs_package_sample-0.1.0.tar.gz
  - Building wheel
  - Built poetry_stabs_package_sample-0.1.0-py3-none-any.whl

Publishing poetry-stabs-package-sample (0.1.0) to testpypi
 - Uploading poetry_stabs_package_sample-0.1.0-py3-none-any.whl FAILED

HTTP Error 403: Invalid or non-existent authentication information. See https://test.pypi.org/help/#invalid-auth for more information. | b'<html>\n <head>\n  <title>403 Invalid or non-existent authentication information. See https://test.pypi.org/help/#invalid-auth for more information.\n \n <body>\n  <h1>403 Invalid or non-existent authentication information. See https://test.pypi.org/help/#invalid-auth for more information.\n  Access was denied to this resource.<br/><br/>\nInvalid or non-existent authentication information. See https://test.pypi.org/help/#invalid-auth for more information.\n\n\n \n'

```

```
poetry config pypi-token.testpypi "pypi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

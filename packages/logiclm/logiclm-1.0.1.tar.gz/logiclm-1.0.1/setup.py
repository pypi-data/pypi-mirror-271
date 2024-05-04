import setuptools

with open("logiclm/README.md", "r") as f:
  long_description = f.read()

setuptools.setup(
  name = "logiclm",
  version = "1.0.1",
  author = "Google LLC",
  author_email = "logica@evgeny.ninja",
  description = "LogicLM",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  url="https://github.com/google/LogicLM",
  packages=setuptools.find_namespace_packages(),
  classifiers = [
      "Topic :: Database",
      "License :: OSI Approved :: Apache Software License"
  ],
  entry_points = {
    # 'console_scripts': ['logiclm=logiclm.logiclm:run_main']
  },
  python_requires= ">=3.0"
)


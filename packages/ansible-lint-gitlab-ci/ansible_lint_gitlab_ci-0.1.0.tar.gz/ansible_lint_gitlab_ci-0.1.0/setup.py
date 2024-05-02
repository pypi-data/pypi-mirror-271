import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ansible-lint-gitlab-ci",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    version="0.1.0",
    author="DevAlphaKilo",
    author_email="DevAlphaKilo@gmail.com",
    description="Converts ansible-lint JSON output into GitLab friendly JUnit XML format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/devalphakilo/ansible-lint-gitlab-ci",
    keywords=['ansible', 'json', 'gitlab', 'ci/cd', 'xml'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": ['ansible-lint-gitlab-ci = ansible_lint_gitlab_ci.main:main']
    },
    install_requires=[
        'ansible-lint>=5.0.7',
    ],
    setup_requires=[],
    python_requires=">=3.6",
)
import setuptools

PACKAGE_NAME = "profile-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.63',  # https://pypi.org/project/profile-local/
    author="Circles",
    author_email="info@circles.life",
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    description="This is a package for sharing common crud operation to profile schema in the db",
    long_description="This is a package for sharing common profile functions used in different repositories",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "database-mysql-local>=0.0.199",
        "logger-local>=0.0.133",
        "location-profile-local>=0.0.18",
        "operational-hours-local>=0.0.19",
        "person-local>=0.0.18",
        "gender-local>=0.0.4",
        "location-local>=0.0.81",
        "reaction-local>=0.0.2",
        "profile-profile-local>=0.0.11",
        "profile-reaction-local>=0.0.16",
        "email-address-local>= 0.0.14",
        "language-remote>=0.0.4",
        "user-context-remote>=0.0.18",
        "storage-local>=0.1.13",
        "group-remote>=0.0.82",
        "group-profile-remote>=0.0.13",
        "python-sdk-local>=0.0.39",
        "visibility-local",
        "shapely>=2.0.2"
    ]
)

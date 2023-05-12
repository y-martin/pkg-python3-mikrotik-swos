from setuptools import setup, find_packages

REQUIREMENTS = [
    "requests"
]

setup(
    name="mikrotik_swos",
    version='0.1',
    description="Mikrotik switch management library",
    author="Yannick Martin",
    author_email="yannick.martin@okazoo.eu",
    url="https://framagit.org/perso4/pkg-python3-mikrotik-swos",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS
)

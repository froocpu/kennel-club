# kennel-club

## What is this?

### Kennel Club

- Kennel Club UK (KCUK) is the UK's largest organisation devoted to dog health, welfare and training.
- Has public data of the lineage of dogs across multiple breeds, going back decades.
- [https://www.thekennelclub.org.uk/](https://www.thekennelclub.org.uk/)

### This repo

- When searching for a particular dog, KCUK limits what you can see in terms of the pedigree for each dog, making exploring the full lineage somewhat tricky.
- For example, asking "Why is my dog yellow when his parents are black?" requires you to explore the ancestry and might require going back multiple generations, which requires a lot of manual trial and error.
- **This project scrapes and collects all the data for a dog's lineage, visualises it in one place and improves the experience of exploring a dog's lineage.**

## Build and run

### Install dependencies

```shell script
pipenv install --dev
```

### Run

With scraping:

```shell script
# Defaults to my dog
pipenv run python get_full_pedigree.py 
```

Without scraping (loads data locally)

```shell script
pipenv run python get_full_pedigree.py --noscrape
```

With a specific dogId:

```shell script
pipenv run python get_full_pedigree.py --start d020bc10-e67b-e911-a8a8-002248005556
```

### d3.js

```shell script
cd d3

# Python3
python -m http.server 8088

# Python2
python -m SimpleHTTPServer 8088
```

Then navigate to your `index.html` at [localhost:8088/index.html](http://localhost:8088/index.html).

## Contributing

### How to contribute

If you do stumble across this and like this:

1. Create a feature branch/fork the project.
2. Submit a merge request/PR with changes.
3. Write some tests if possible and make sure everything builds/passes properly.

### TODO

- [x] Crawls through ancestry to find more dogs until it hits a wall (a dog with no available profile.)
- [x] Scrape more information from each dog profile.
- [ ] Get more data for litters produced and convert it into nodes and links. 
- [x] First visualisation in D3. 
- [ ] Convert JSON files to CSV for to save space.
- [ ] Polish D3.js visualisation
- [ ] Automate build and tests.
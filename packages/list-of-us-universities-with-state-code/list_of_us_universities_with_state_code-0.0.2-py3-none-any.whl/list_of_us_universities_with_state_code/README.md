# Package: us_universities_with_state_codes

This package consists of the list of all top US universities along with their state codes, and basic retrieval functions in python.


## Usage/Examples

```python
# This function will return the array of all the universities
get_universities()
```

```python
# This function will return the object -> university name as the key and state code as value
get_state_code_of_university("mit")

#Output:
{'Massachusetts Institute of Technology (MIT)': 'MA'}
```

```python
# This function will return the array of all the universities in the given state code
get_universities_by_state_code("CA")

#Output:
{'Stanford': 'CA', 'California Institute of Technology (Caltech)': 'CA', 'University of California, Berkeley (UC Berkeley)': 'CA', 'University of California, Los Angeles (UCLA)': 'CA', ...}
```

## Tech Stack

**Library:** Python


## License

[MIT](https://choosealicense.com/licenses/mit/)


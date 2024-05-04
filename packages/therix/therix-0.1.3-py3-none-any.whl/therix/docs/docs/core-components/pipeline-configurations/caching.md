---
slug: /components/pipeline-config/caching
sidebar_position: 15
---

# Caching

Therix provides an optional caching layer for Language Model (LM) requests. This caching layer offers two primary benefits:

- **Cost Reduction**: By caching LM responses, Therix reduces the number of API calls made to the LM provider, saving you money, especially when frequently requesting the same completions.
  
- **Improved Application Performance**: The caching layer also enhances application speed by minimizing the number of API calls made to the LM provider, resulting in faster response times and reduced latency.

Therix supports two types of Caching :- 


## Exact Match Caching

- Exact Match Caching involves storing and retrieving data based on exact key-value pairs. 
- In Therix - Exact Match Caching helps optimize performance by quickly retrieving frequently accessed completions without the need for repeated API calls to the LM provider.

## Semantic Caching


- Semantic Caching extends caching beyond exact matches and considers the meaning or context of the data being cached.
- In Therix, Semantic Caching intelligently caches data based on its semantic relevance, enhancing the efficiency of LM requests and reducing overall resource utilization.



## Adding Caching to Your Pipeline

You can easily add caching to your pipeline configuration by including the following line while creating the pipeline:

```python
.add(CacheConfig(config={}))
```

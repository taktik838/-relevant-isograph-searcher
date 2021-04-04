# isograph-searcher

## How starts
First, you need to get secret.json for google([instructions](https://cloud.google.com/speech-to-text/docs/quickstart-protocol?hl=en_US#before_you_begin)). 
Need only get secret.json(only complete "Before you begin" step 1). Then put this file to src/integrations/google/secret.json.
Then you can typing to console
```bash
docker-compose up
```
Will be started:
* isolated:
  * elasticsearch
  * redis
  * tensorflow_serving
* no isolated:
  * isograph-searcher service

After starting you can find swaggers:
* http://localhost:8085/api/swagger



# Observabilidade DataDog e CloudWatch para Glue Job (o11y-dd-cw)

Esse projeto tem como objetivo gerar métricas para DataDog via API e para CloudWatch usando boto3.

Apesar do envio de métricas para DataDog estar mais maduto, mesmo assim é bem simples. Usando o endpoint series da API do DataDog.

No cloudWath, é basicamente um count.


## Usando a lib no AWS Glue

### Criando Arquivo para deploy

Basicamente basta compactar a pasta DataObservability. Por exemplo DataObservability.zip

Preferencialmente usem compactação zip.


### Criando Bucket S3

É necessário criar um bucket S3 para que gravado o módulo python em zip (DataObservability.zip).

Quando cliado, faça o uploado do DataObservability.zip, para o bucket. 

Quando for referenciar o módulo no Glue Job, use a S3 URI.

### Configuando o Glue Job

Dentro do console da AWS (Glue), vá até Visual ETL -> Na lista de jobs, clique no job onde deseja aplicar.

Já dentro do Job, clique em Job details, abra as opções Advanced Properties e role até Libraries e no campo Python Library Path e forneça o caminho do arquivo zip que contém a lib.

exemplo do conteúdo: s3://glue-python-3-libs/DataObservability.zip

### Como implementar o módulo

#### Import
```python

from DataObservability.Metrics.datadog import config, series, reset_start_time

```


#### Config

```python

config(job_name="entregas_full", tags=["env:local"], retry=2)

```
#### Resources e Tags

```python

resources = [{"name": "glue_job_teste", "type": "glue_job_teste"}]
tags = ["lab:true"]

```

#### Enviar métrica

```python

@series(metric="execution.success.count", resources=resources, tags=tags)
def f1(nome, sobrenome):
    print(f"success -> {nome} - {sobrenome}")

```

* No repo tem um exemplo completo teste.py
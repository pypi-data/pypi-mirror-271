# Python SDK to use the Hectiq Lab

## Objectifs de la révision
- Créer un format fonctionnel.
- Créer un format orienté objet.
- Utiliser les ContextVar.
- Bonifier le CLI pour supporter la plupart des commandes.
- Réviser l'objet de configuration pour le rendre quasi-natif à Python.


## Style

- Utiliser le moins possible de classes conçues pour être exposées au client. Le Lab doit utiliser des objets natifs au maximum pour simplifier son utilisation.
- Faire du code le plus simple possible.
- Le lab doit intégrer le moins possibles de dépendances externes (favoriser les dépendances robustes et legacy).
- Les fonctions sont documentés dans le script et dans l'application de documentation.
- Le Lab doit avalé les erreurs si l'API ne répond pas, si une erreur survient ou si le Wifi est down.
- Le lab ne doit pas ralentir un script (asynchrone).


## Examples

### Functional

#### Create a training run

```python
import pyhectiqlab.functional import hl

# Skip this if the project is already set using `hectiqlab_config.toml`
hl.set_project("hortau/irrigation")
hl
with Run(block="Test") as run:
    execeute()
    print(Run.block)
    block = hl.get_block()
    model = hl.Model.create()

```


## Modifications suggérées
- Dans MEtricsManager, Modifier les warning pour gérer la référence à `run.set_metrics_aggr('mean')`é
- Enlever. On ne  raise ValueError("You are not logged in. Please login first.")
- Gérer les API_URL
- Lazy init de Auth.
- S'assurer que ça marche sans authentification.
# Site TAMUDA INJAD – HTML5 / CSS3 / JS natif

Site multipage statique (23 pages + modèle d’article), sans framework ni dépendance externe, sans police distante, sans traceur.

## Prévisualiser en local
Les liens sont en chemins absolus depuis la racine (`/services/…`) : servez le dossier **à la racine** d’un serveur.
```
cd tamuda-injad
python3 -m http.server 8000      # puis ouvrir http://localhost:8000/
```
(ouvrir les fichiers par double-clic ne fonctionne pas correctement avec des liens absolus.)

## Modifier le site
Le contenu et les informations de l’entreprise sont centralisés dans `build.py` (bloc `CFG`). Le script régénère toutes les pages (header/footer écrits dans le HTML de chaque page).
```
python3 build.py
```
Les fichiers HTML livrés sont déjà générés ; vous pouvez aussi les éditer à la main.

## Logo
Le fichier fourni est un **PNG transparent** : il est placé dans `assets/images/tamuda-logo.png` (et non `.jpg`). Il n’est ni recoloré, ni recadré, ni déformé (ratio 1270×1124 conservé via width/height + aspect-ratio).

## Informations à renseigner avant publication
Pays, ville, adresse, code postal, zones réellement desservies, téléphone (format international), e-mail, domaine final, horaires confirmés, agréments et autorisations vérifiés, informations juridiques (éditeur, hébergeur…), coordonnées GPS, lien Google Maps (et éventuelle intégration), lien d’avis clients, numéro des secours du pays, confirmation de la disponibilité 24h/24 (`AVAIL_24H`), présence de personnel médical et équipements (pages Transport médicalisé, Patient alité, Rapatriement, Événementiel). Tous les champs manquants apparaissent en jaune : `[À COMPLÉTER : …]`.

## Mise en ligne (étapes)
1. Renseigner `CFG` dans `build.py` (au minimum `DOMAIN`), puis `python3 build.py`.
2. Contrôler qu’aucun `[À COMPLÉTER` ne reste : `grep -r "À COMPLÉTER" --include=*.html .`
3. Passer `INDEXABLE=True` puis relancer `build.py` (retire `noindex`, autorise `robots.txt`, finalise sitemap).
4. Déployer le dossier à la racine du domaine ; configurer la page 404 (`/404.html`) sur l’hébergeur et HTTPS.
5. Soumettre `sitemap.xml` dans les outils webmaster.

**État par défaut :** `INDEXABLE=False` → `<meta robots noindex>` et `robots.txt` en `Disallow: /` (site en préparation).
**JSON-LD / canonical / og:url / sitemap :** générés avec des URL absolues seulement si `DOMAIN` est renseigné ; aucune valeur fictive n’est publiée. Le type `Organization` est volontairement générique : le remplacer par un type plus précis (ex. `LocalBusiness`) seulement une fois les activités et données confirmées. Aucun avis, note ni SearchAction.

## Formulaires (devis, contact, zone)
Sans backend, les formulaires sont en **mode démonstration** : validation accessible, message explicite, **aucune transmission, aucun stockage**, pas de faux « envoyé ».
Pour les activer : renseigner `FORM_ENDPOINT` (URL HTTPS d’un service sécurisé de réception : backend maison ou service de formulaires conforme à votre pays). Le JS envoie alors un JSON via `fetch` et n’affiche « transmise » que si le serveur répond `2xx`. Un champ leurre anti-spam est ajouté dans ce mode ; prévoir côté serveur validation, limitation de débit et CORS. Aucune clé secrète ne doit figurer dans le code.

## Carte
Sans `MAPS_EMBED`, seul un emplacement et une alternative textuelle s’affichent. Avec une URL d’intégration, l’iframe ne se charge qu’**après clic**. Mettre à jour la politique de confidentialité en conséquence.

## Checklist SEO / vérifications manuelles
- [ ] Chaque page : `title` et `meta description` uniques, un seul H1 (script de contrôle ou extension navigateur).
- [ ] Canonical absolue = URL finale, avec slash final, HTTPS.
- [ ] `sitemap.xml` : toutes les URL répondent 200 ; `robots.txt` pointe vers le sitemap.
- [ ] JSON-LD valide (outil de test Schema.org / Rich Results) et sans champ `[À COMPLÉTER]`.
- [ ] JSON-LD FAQPage = questions visibles sur la page.
- [ ] Liens tél. et e-mail testés sur mobile ; NAP identique partout.
- [ ] Navigation au clavier (menu, sous-menu Services, formulaires), lecteur d’écran, zoom 200 %, contrastes.
- [ ] Test sur mobiles réels ; mesure des performances (Lighthouse/PageSpeed) – **non réalisée**.
- [ ] Relecture juridique des pages légales selon le pays.

## Limites et tests non exécutés
Contenus rédigés sans informations vérifiées sur l’entreprise : à relire et valider. Pages légales = trames, sans garantie de conformité. Aucun test de performance, SEO ou d’accessibilité automatisé n’a été effectué ; un contrôle des liens internes, un test de débordement horizontal sur la page d’accueil en mobile (390 px) et le comportement des formulaires en mode démonstration ont été vérifiés dans un navigateur de test. Aucun classement Google n’est garanti.

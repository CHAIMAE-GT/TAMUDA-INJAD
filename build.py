#!/usr/bin/env python3
"""Générateur du site TAMUDA INJAD (HTML/CSS/JS statique).
Modifiez CFG ci-dessous, puis lancez :  python3 build.py
Le header/footer sont écrits dans le HTML de chaque page (aucune injection JS).

SEO intégré :
- JSON-LD sur chaque page : WebPage + BreadcrumbList + schémas métier
  (LocalBusiness/Organization, Service, FAQPage, BlogPosting, ItemList…)
- <head> enrichi : canonical, Open Graph complet (og:image + alt), Twitter Card,
  geo.placename pour le référencement local, robots explicites.
- sitemap.xml priorisé (priority + changefreq + lastmod) et robots.txt propres."""
import os, json, html, re, datetime
ROOT = os.path.dirname(os.path.abspath(__file__))

# ───────────── CONFIGURATION (à compléter avec les vraies informations) ─────────────
'''CFG = dict(
    DOMAIN="",
    INDEXABLE=False,
    COUNTRY="Maroc", CITY="Tétouan", ADDRESS="", POSTAL="",
    AREAS=["Tétouan", "Martil", "M'diq", "Chefchaouen", "Tanger", "Fahs-Anjra", "Rabat", "Casablanca"],
    PHONE_INTL="",
    PHONE_DISPLAY="",
    EMAIL="", HOURS="",
    EMERGENCY_NUMBER="",
    MAPS_LINK="", MAPS_EMBED="",
    REVIEWS_LINK="",
    FORM_ENDPOINT="https://formspree.io/f/mbgoagop",
    REVIEWS_ENDPOINT="https://formspree.io/f/xaeodebv",  # ← nouveau formulaire Formspree
    AVAIL_24H=False,
    LEGAL={},
) '''


CFG = dict(
    # ==========================================
    # TAMUDA INJAD — CONFIGURATION DE TEST
    # ==========================================

    # Identité et domaine
    BUSINESS_NAME="TAMUDA INJAD",
    DOMAIN="https://tamuda-injad.netlify.app",
    INDEXABLE=False,  # Ne pas indexer pendant les tests

    # Localisation
    COUNTRY="Maroc",
    CITY="Tétouan",
    ADDRESS="",       # À compléter après validation
    POSTAL="",

    # Zones d'intervention prévues
    AREAS=[
        "Tétouan",
        "Martil",
        "M'diq",
        "Chefchaouen",
        "Tanger",
        "Fahs-Anjra",
        "Rabat",
        "Casablanca",
    ],

    # Coordonnées officielles à renseigner
    PHONE_INTL="",
    PHONE_DISPLAY="",
    EMAIL="",

    # Disponibilité et urgences
    HOURS="",
    EMERGENCY_NUMBER="",
    AVAIL_24H=False,

    # Google Maps
    MAPS_LINK="",
    MAPS_EMBED="",

    # Avis et témoignages
    REVIEWS_LINK="",

    # Formulaires Formspree
    FORM_ENDPOINT="https://formspree.io/f/mbgoagop",
    REVIEWS_ENDPOINT="https://formspree.io/f/xaeodebv",

    # Informations légales
    LEGAL={},

    # Mode de démonstration
    TEST_MODE=True,
)


NAME = "TAMUDA INJAD"
TODAY = datetime.date.today().isoformat()
LOGO = "/assets/images/tamuda-logo.png"
E = html.escape
def todo(l): return f'<span class="todo">[À COMPLÉTER : {E(l)}]</span>'
def val(k, l): return E(CFG[k]) if CFG[k] else todo(l)
def absu(p): return CFG["DOMAIN"] + p
CONF = bool(CFG["DOMAIN"])
def strip(h): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h)).strip()

def call_btn(cls="btn btn-primary", txt="Appeler"):
    if CFG["PHONE_INTL"]: return f'<a class="{cls}" href="tel:{E(CFG["PHONE_INTL"])}">{txt}</a>'
    return f'<a class="{cls}" href="/contact/">{txt} <small>(n° à compléter)</small></a>'
def quote_btn(cls="btn btn-secondary"): return f'<a class="{cls}" href="/tarifs-devis/">Demander un devis</a>'
def ctas(): return f'<div class="btn-row">{call_btn()}{quote_btn()}</div>'

# ───────────── DONNÉES : SERVICES ─────────────
def eq_note(extra=""):
    return (f'<div class="notice warn"><p><strong>Équipements et accompagnement :</strong> {extra}'
            f'{todo("lister uniquement les équipements et le personnel d’accompagnement confirmés")}</p></div>')

SERVICES = [
dict(slug="ambulance-24h-24", name="Ambulance 24h/24",
 short="Faire une demande de transport en dehors des horaires habituels, selon la disponibilité confirmée par l’entreprise.",
 h1="Ambulance 24h/24 : demander un transport à toute heure",
 intro="Un transfert décidé en fin de journée, une sortie d’hôpital tardive, un trajet un dimanche : tous les transports ne se planifient pas à l’avance. Cette page explique comment formuler une demande en dehors des horaires de bureau et ce qu’il est utile d’avoir sous la main.",
 notice="Disponibilité 24h/24, week-ends et jours fériés : " + todo("à confirmer avant publication — jours et horaires réels"),
 scope="Ce service concerne les demandes de transport en ambulance formulées de jour comme de nuit, y compris le week-end et les jours fériés, dans la mesure où l’entreprise les assure. Il ne s’agit pas d’un service public d’urgence et il ne remplace pas les secours compétents.",
 situations=["Sortie d’hospitalisation en soirée ou le week-end.","Transfert entre établissements décidé tardivement.","Trajet programmé très tôt le matin.","Retour à domicile un jour férié."],
 orga=[("Votre demande","Indiquez le lieu de prise en charge, la destination et l’heure souhaitée."),("Vérification","L’équipe vérifie la faisabilité : disponibilité, distance, zone desservie."),("Confirmation","L’heure de prise en charge et l’interlocuteur vous sont confirmés."),("Trajet","Le transport est réalisé ; l’équipe reste joignable pour les ajustements.")],
 prep=["Adresse précise de départ (étage, accès, code d’entrée).","Établissement et service de destination.","Heure souhaitée et souplesse éventuelle.","Nom et numéro d’une personne joignable sur place.","Documents éventuellement demandés (à confirmer auprès de l’entreprise)."],
 faq=[("Puis-je réserver la nuit ou le week-end ?","Cela dépend des disponibilités réellement assurées par l’entreprise. Contactez-la directement : elle vous indiquera si votre demande peut être prise en charge."),("Est-ce un service d’urgence ?","Non. En cas d’urgence vitale, contactez sans attendre les secours compétents de votre pays.")],
 rel=["transfert-hospitalier","transport-medicalise","patient-alite-fauteuil-roulant"]),
dict(slug="transport-medicalise", name="Transport médicalisé",
 short="Un transport accompagné d’une surveillance médicale ou paramédicale, lorsque cela a été indiqué par un professionnel de santé.",
 h1="Transport médicalisé : comprendre et préparer la demande",
 intro="« Médicalisé » ne veut pas dire « en ambulance » : le terme désigne un transport pendant lequel une équipe médicale ou paramédicale assure une surveillance. Cette page aide à situer cette prestation par rapport aux autres et à préparer votre demande.",
 notice="Présence d’un médecin, d’un infirmier et équipements embarqués : " + todo("à confirmer avant toute publication"),
 scope="Le transport médicalisé se distingue du transport en fauteuil roulant ou d’un transport allongé sans surveillance particulière. Son périmètre exact (personnel, matériel, conditions) dépend de ce que l’entreprise est autorisée et en mesure d’assurer. Seul un professionnel de santé peut indiquer si ce type de transport est nécessaire.",
 situations=["Un médecin ou un établissement a indiqué qu’une surveillance est nécessaire pendant le trajet.","Transfert vers un établissement spécialisé avec prise en charge organisée en amont.","Besoin de coordination entre l’équipe de départ et celle d’accueil."],
 orga=[("Indication","La nécessité du transport médicalisé est établie par un professionnel de santé, pas par ce site."),("Demande","Vous communiquez les informations logistiques : lieux, horaires, établissement."),("Coordination","L’entreprise confirme ce qu’elle peut assurer et échange avec les parties concernées."),("Transport","Le trajet est réalisé selon les modalités convenues.")],
 prep=["Prescription ou demande de l’établissement, si elle existe (à transmettre par un canal sécurisé, jamais dans un champ libre).","Coordonnées du service de départ et d’accueil.","Horaire visé et contraintes d’accès."],
 faq=[("Un médecin est-il présent dans le véhicule ?","Cette information doit être confirmée par l’entreprise pour chaque transport. Ne la considérez pas comme acquise sans confirmation écrite."),("Qui décide qu’un transport doit être médicalisé ?","Un professionnel de santé. TAMUDA INJAD n’établit ni diagnostic ni indication médicale.")],
 rel=["transfert-hospitalier","rapatriement-sanitaire","ambulance-24h-24"], eq=True),
dict(slug="transfert-hospitalier", name="Transfert hospitalier",
 short="Organiser un trajet entre deux établissements de santé ou entre un établissement et le domicile.",
 h1="Transfert hospitalier : d’un établissement à un autre",
 intro="Un transfert implique toujours plusieurs interlocuteurs : le service qui envoie, celui qui accueille, parfois la famille. Bien préparer les informations logistiques évite les attentes inutiles le jour J.",
 scope="Trajets entre établissements de santé, retours à domicile après hospitalisation et transferts vers des consultations ou examens spécialisés, selon les prestations réellement proposées par l’entreprise.",
 situations=["Changement d’établissement ou de service.","Retour à domicile après une hospitalisation.","Rendez-vous spécialisé dans un autre établissement.","Entrée en établissement de soins de suite ou en hébergement médicalisé."],
 orga=[("Coordonnées","Rassemblez les noms des établissements, services et contacts de chaque côté."),("Horaire","Convenez d’un créneau compatible avec l’équipe de départ et d’accueil."),("Prise en charge","L’équipe vient chercher la personne à l’endroit et à l’heure convenus."),("Remise","À l’arrivée, la personne est confiée à l’équipe d’accueil.")],
 prep=["Nom de l’établissement de départ, service, étage, chambre.","Nom de l’établissement d’accueil et service.","Heure de sortie prévue et heure d’arrivée attendue.","Contact joignable (famille ou personnel).","Documents demandés par les établissements (à vérifier avec eux)."],
 faq=[("Qui prévient l’établissement d’accueil ?","Cela varie selon les situations. Précisez-le lors de la demande afin de répartir clairement les rôles."),("Un proche peut-il accompagner ?","Cela dépend des règles de l’entreprise et du véhicule ; demandez confirmation avant le jour du transport.")],
 rel=["patient-alite-fauteuil-roulant","transport-medicalise","dialyse-chimiotherapie"]),
dict(slug="patient-alite-fauteuil-roulant", name="Patient alité / fauteuil roulant",
 short="Un transport adapté à la mobilité de la personne : allongée ou en fauteuil roulant, selon les moyens disponibles.",
 h1="Transport de personne alitée ou en fauteuil roulant",
 intro="Allongée, assise, en fauteuil : la manière de voyager dépend de la mobilité de la personne et de l’accès aux lieux. Ces deux situations ne sont pas équivalentes et ne s’organisent pas de la même façon ; cette page aide à les distinguer.",
 scope="Transport de personnes ne pouvant pas se déplacer seules, soit en position allongée, soit en fauteuil roulant. Les véhicules, équipements et modalités de transfert disponibles doivent être confirmés par l’entreprise ; une personne en fauteuil n’est pas automatiquement transportée dans les mêmes conditions qu’une personne alitée.",
 situations=["Rendez-vous médical d’une personne à mobilité réduite.","Retour à domicile avec des escaliers ou un ascenseur étroit.","Déplacement familial ou administratif d’une personne en fauteuil."],
 orga=[("Description de la mobilité","Précisez simplement : allongé, fauteuil manuel ou électrique, aide nécessaire pour le transfert."),("Repérage des accès","Étage, ascenseur, largeur des portes, marches, distance au stationnement."),("Choix du moyen","L’entreprise indique le véhicule adapté parmi ceux dont elle dispose."),("Trajet","Prise en charge au point convenu et remise à destination.")],
 prep=["Type de fauteuil (manuel, électrique) et, si utile, son encombrement.","Présence d’escaliers, d’un ascenseur, largeur d’accès.","Besoin d’aide pour le transfert lit/fauteuil.","Présence d’un accompagnant."],
 faq=[("Mon fauteuil électrique peut-il être transporté ?","Cela dépend du véhicule et du fauteuil. Communiquez le type de fauteuil et demandez confirmation."),("Faut-il décrire l’état de santé ?","Non. Décrivez seulement la mobilité et les accès, sans informations médicales détaillées.")],
 rel=["transfert-hospitalier","dialyse-chimiotherapie","ambulance-evenementielle"], eq=True),
dict(slug="dialyse-chimiotherapie", name="Dialyse & chimiothérapie",
 short="Organiser des trajets réguliers vers un centre de soins, avec un planning et un interlocuteur identifiés.",
 h1="Trajets réguliers pour dialyse et chimiothérapie",
 intro="Quand les séances reviennent chaque semaine, le transport devient une routine à organiser : mêmes horaires, même point de prise en charge, même interlocuteur. Cette page décrit l’aspect pratique de ces trajets, sans aucun conseil médical.",
 scope="Transports récurrents vers un établissement ou centre de soins pour des séances programmées. Les modalités (fréquence, prise en charge administrative, tarification) doivent être confirmées avec l’entreprise ; aucune prise en charge ou remboursement n’est annoncé ici.",
 situations=["Séances programmées plusieurs fois par semaine ou par mois.","Changement ponctuel d’horaire ou de lieu de séance.","Besoin d’un planning partagé avec la famille."],
 orga=[("Planning","Communiquez les jours, les horaires de séance et le lieu."),("Mise en place","L’entreprise propose une organisation récurrente selon ses disponibilités."),("Suivi","Un interlocuteur est désigné pour signaler tout changement."),("Ajustements","En cas d’annulation ou de report de séance, prévenez l’équipe dès que possible.")],
 prep=["Calendrier des séances et horaires de début.","Adresse du centre et point de prise en charge.","Durée d’attente souhaitée au retour, si besoin.","Coordonnées d’une personne joignable."],
 faq=[("Puis-je prévoir tout un mois à l’avance ?","Cela dépend de l’organisation de l’entreprise. Demandez comment sont gérés les plannings récurrents."),("Que faire si une séance est reportée ?","Prévenez l’entreprise dès que possible afin qu’elle adapte le planning ; le délai attendu est à confirmer avec elle.")],
 rel=["transfert-hospitalier","patient-alite-fauteuil-roulant","ambulance-24h-24"]),
dict(slug="rapatriement-sanitaire", name="Rapatriement sanitaire",
 short="Préparer une demande de rapatriement : un transport complexe impliquant souvent plusieurs acteurs.",
 h1="Rapatriement sanitaire : ce qu’il faut organiser",
 intro="Un rapatriement sanitaire dépasse le simple trajet : il implique des établissements, des échanges administratifs et parfois des assurances ou assistances. L’objectif de cette page est de poser les bonnes questions dès le départ.",
 notice="Rapatriements assurés (destinations, moyens, partenaires) : " + todo("à confirmer avant publication"),
 scope="Organisation du retour d’une personne depuis un lieu éloigné vers un établissement ou son domicile. Les destinations, moyens de transport et autorisations nécessaires dépendent de l’entreprise, des pays concernés et des partenaires éventuels ; rien ne doit être présumé tant que ces éléments ne sont pas validés.",
 situations=["Retour vers l’établissement ou le domicile après un séjour éloigné.","Dossier impliquant une assurance ou une assistance.","Besoin de coordination entre plusieurs établissements."],
 orga=[("Premier contact","Indiquez le lieu actuel, la destination souhaitée et l’échéance."),("Étude de faisabilité","L’entreprise détermine ce qu’elle peut assurer et avec quels partenaires."),("Coordination","Échanges avec les établissements et, le cas échéant, l’assurance."),("Transport","Réalisation selon le plan convenu.")],
 prep=["Lieu actuel et destination souhaitée.","Coordonnées de l’établissement concerné.","Coordonnées de l’assurance ou de l’assistance, si elle existe.","Échéance souhaitée."],
 faq=[("Le rapatriement vers l’étranger est-il possible ?","Cela dépend des autorisations et des moyens de l’entreprise. Demandez une confirmation écrite avant tout engagement."),("Qui règle les démarches administratives ?","La répartition doit être précisée dès le premier échange avec l’entreprise et les autres parties.")],
 rel=["transport-medicalise","transfert-hospitalier","ambulance-24h-24"], eq=True),
dict(slug="ambulance-evenementielle", name="Ambulance événementielle",
 short="Prévoir la présence d’une ambulance sur un événement, selon la réglementation et les moyens confirmés.",
 h1="Ambulance événementielle : préparer la présence sur site",
 intro="Compétition sportive, spectacle, rassemblement : les organisateurs sont parfois amenés à prévoir un dispositif de secours sur place. Cette page liste les informations à rassembler pour étudier une demande.",
 notice="Conditions et obligations réglementaires applicables aux événements : " + todo("à vérifier selon le pays et les autorités locales"),
 scope="Étude d’une présence d’ambulance lors d’un événement, dans les limites de ce que l’entreprise peut légalement et matériellement assurer. L’organisateur reste responsable de ses obligations vis-à-vis des autorités compétentes.",
 situations=["Événement sportif ou culturel.","Rassemblement public ou privé nécessitant un dispositif.","Chantier ou tournage nécessitant une présence ponctuelle."],
 orga=[("Cadrage","Date, lieu, durée, nombre de participants attendus."),("Étude","Examen du dispositif possible et des contraintes réglementaires."),("Plan d’accès","Définition de l’emplacement et des accès pour les véhicules."),("Présence","Mise en place le jour de l’événement selon l’accord.")],
 prep=["Nature, date et durée de l’événement.","Adresse précise et plan d’accès.","Nombre de participants attendus.","Coordonnées de l’organisateur référent.","Éventuelles exigences des autorités locales."],
 faq=[("Un devis est-il nécessaire ?","Oui, une étude est nécessaire pour définir le dispositif ; consultez la page Tarifs & devis."),("L’ambulance peut-elle quitter l’événement en cas de transport ?","Les modalités de continuité du dispositif doivent être convenues à l’avance avec l’entreprise.")],
 rel=["ambulance-24h-24","transport-medicalise","patient-alite-fauteuil-roulant"], eq=True),
]
SBY = {s["slug"]: s for s in SERVICES}

# ───────────── DONNÉES : FAQ ─────────────
FAQ = [
("Réservation et délais",[
 ("Comment faire une demande de transport ?","Utilisez le formulaire de la page Tarifs & devis ou contactez l’entreprise avec les coordonnées de la page Contact. Indiquez le lieu de départ, la destination, la date souhaitée et un numéro pour vous rappeler."),
 ("Quel délai prévoir avant un transport programmé ?","Plus la demande est faite tôt, plus l’organisation est simple. Le délai minimum dépend des disponibilités de l’entreprise et doit être confirmé directement avec elle."),
 ("Peut-on réserver pour le jour même ?","Cela dépend des disponibilités du moment. Contactez l’entreprise, qui vous dira si la demande peut être prise en charge."),
 ("Comment modifier ou annuler une demande ?","Prévenez l’entreprise le plus tôt possible par téléphone. Les conditions d’annulation éventuelles doivent vous être communiquées lors de la confirmation."),
 ("Les demandes sont-elles possibles la nuit et le week-end ?","Les horaires d’intervention sont à confirmer auprès de l’entreprise. Consultez la page Ambulance 24h/24 pour plus d’informations.")]),
("Devis et tarifs",[
 ("Comment obtenir un devis ?","Remplissez le formulaire de devis ou contactez l’entreprise. Le devis est établi à partir du trajet, de la date et du type de transport."),
 ("Quels éléments influencent le prix ?","Généralement : la distance, le type de transport, les horaires, l’accompagnement éventuel et les contraintes d’accès. Le détail est précisé dans le devis."),
 ("Une prise en charge ou un remboursement est-il possible ?","Cela dépend de votre situation et des règles applicables dans votre pays. Renseignez-vous auprès de l’organisme concerné ; ce site ne garantit aucune prise en charge."),
 ("Le devis est-il gratuit ?","Les conditions d’établissement du devis doivent être confirmées par l’entreprise lors de votre demande.")]),
("Documents et informations",[
 ("Quels documents dois-je préparer ?","Les documents demandés varient selon la situation et les règles locales. L’entreprise ou l’établissement concerné vous indiquera lesquels sont utiles."),
 ("Dois-je envoyer des informations médicales ?","Non, pas dans les formulaires de ce site. Ne saisissez aucun diagnostic ni détail de santé dans un champ libre ; l’entreprise vous dira par quel canal transmettre un document si nécessaire."),
 ("Où sont utilisées mes données personnelles ?","Elles servent à traiter votre demande. Consultez la Politique de confidentialité pour le détail.")]),
("Accompagnants et déroulement",[
 ("Un proche peut-il m’accompagner ?","Selon le véhicule et le type de transport. Demandez confirmation avant le jour du trajet."),
 ("Que se passe-t-il à l’arrivée ?","La personne est confiée à l’équipe de l’établissement ou à la personne attendue, selon ce qui a été convenu à l’avance."),
 ("Faut-il être présent au moment du départ ?","Il est préférable qu’une personne joignable soit disponible au point de prise en charge. Précisez-le lors de la demande."),
 ("Comment est organisé l’accès au domicile ?","Indiquez l’étage, la présence d’un ascenseur, les marches éventuelles et le code d’accès pour faciliter l’intervention.")]),
("Trajets réguliers",[
 ("Peut-on organiser des trajets récurrents ?","Oui, sous réserve des disponibilités de l’entreprise. Communiquez le calendrier et le lieu pour étudier la mise en place."),
 ("Comment signaler un changement de planning ?","Contactez l’entreprise dès que possible. Le délai attendu est à confirmer avec elle."),
 ("Peut-on avoir toujours le même interlocuteur ?","Demandez-le lors de la mise en place du planning ; l’entreprise vous indique ce qui est possible.")]),
("Services et urgence",[
 ("TAMUDA INJAD est-elle un service d’urgence ?","Non. En cas d’urgence vitale, contactez immédiatement les secours compétents de votre pays."),
 ("Quelle différence entre fauteuil roulant, transport sanitaire et transport médicalisé ?","Ce sont des prestations distinctes : le fauteuil concerne la mobilité, le transport sanitaire un trajet en ambulance, le transport médicalisé une surveillance médicale pendant le trajet. Consultez la page de chaque service."),
 ("Ce site donne-t-il des conseils médicaux ?","Non. Il fournit des informations pratiques sur l’organisation des transports, jamais de diagnostic ni de conseil thérapeutique.")]),
]
FAQ_FLAT = [qa for _, qs in FAQ for qa in qs]

# ───────────── BLOC COMMUN ─────────────
NAVLINKS = [("Accueil","/"),("Services","/services/"),("Zone & carte","/zone-intervention/"),("Tarifs & devis","/tarifs-devis/"),("Témoignages","/temoignages/"),("Blog","/blog/"),("FAQ","/faq/"),("À propos","/a-propos/"),("Contact","/contact/")]
def cur(cp, p):
    current = cp == p or (p == "/blog/" and cp.startswith(p))
    return ' aria-current="page"' if current else ""

def header(cp):
    li = []
    for lab, p in NAVLINKS:
        if lab == "Services":
            sub = "".join(f'<li><a href="/services/{s["slug"]}/"{cur(cp, "/services/%s/" % s["slug"])}>{E(s["name"])}</a></li>' for s in SERVICES)
            li.append(f'<li class="has-sub"><div class="sub-row"><a class="nav-link" href="/services/"{cur(cp,p)}>Services</a>'
                      f'<button class="sub-toggle" type="button" aria-expanded="false" aria-controls="submenu-services"><span class="sr-only">Afficher les sept prestations</span></button></div>'
                      f'<ul class="submenu" id="submenu-services">{sub}</ul></li>')
        else:
            li.append(f'<li><a class="nav-link" href="{p}"{cur(cp,p)}>{E(lab)}</a></li>')
    emerg = (f'En cas d’urgence vitale, contactez immédiatement les secours compétents de votre pays ({CFG["EMERGENCY_NUMBER"]}).' if CFG["EMERGENCY_NUMBER"]
             else f'En cas d’urgence vitale, contactez immédiatement les secours compétents de votre pays {todo("numéro d’urgence du pays")}.')
    phone = (f'<a href="tel:{E(CFG["PHONE_INTL"])}">{E(CFG["PHONE_DISPLAY"] or CFG["PHONE_INTL"])}</a>' if CFG["PHONE_INTL"] else f'Téléphone : {todo("numéro")}')
    return f'''<a class="skip-link" href="#contenu">Aller au contenu principal</a>
<div class="urgent" role="note"><div class="container"><strong>Urgence vitale ?</strong> {emerg} {NAME} n’est pas un service public d’urgence.</div></div>
<div class="topbar"><div class="container"><span>{phone}</span></div></div>
<header class="site-header"><div class="container">
<a class="brand" href="/" aria-label="{NAME} – retour à l’accueil"><img src="{LOGO}" width="72" height="64" alt="Logo {NAME} : une ambulance sur une route de montagne"></a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav"><span>Menu</span></button>
<nav class="site-nav" id="primary-nav" aria-label="Navigation principale"><ul>{"".join(li)}<li class="nav-cta">{call_btn("btn btn-primary")}</li></ul></nav>
</div></header>'''

def footer():
    svc = "".join(f'<li><a href="/services/{s["slug"]}/">{E(s["name"])}</a></li>' for s in SERVICES)
    return f'''<footer class="site-footer"><div class="container">
<div class="footer-grid">
<div><img src="{LOGO}" width="140" height="124" alt="Logo {NAME}" loading="lazy"><p class="meta">Transport en ambulance. Les informations pratiques sont à confirmer directement avec l’entreprise.</p></div>
<div><h2>Services</h2><ul>{svc}</ul></div>
<div><h2>Le site</h2><ul><li><a href="/zone-intervention/">Zone &amp; carte</a></li><li><a href="/tarifs-devis/">Tarifs &amp; devis</a></li><li><a href="/faq/">FAQ</a></li><li><a href="/a-propos/">À propos</a></li><li><a href="/temoignages/">Témoignages</a></li><li><a href="/blog/">Blog</a></li><li><a href="/contact/">Contact</a></li></ul></div>
<div><h2>Contact</h2><address style="font-style:normal"><p>{NAME}<br>{val("ADDRESS","adresse")}<br>{val("POSTAL","code postal")} {val("CITY","ville")}<br>{val("COUNTRY","pays")}</p>
<p>Tél. : {f'<a href="tel:{E(CFG["PHONE_INTL"])}">{E(CFG["PHONE_DISPLAY"] or CFG["PHONE_INTL"])}</a>' if CFG["PHONE_INTL"] else todo("téléphone")}<br>
E-mail : {f'<a href="mailto:{E(CFG["EMAIL"])}">{E(CFG["EMAIL"])}</a>' if CFG["EMAIL"] else todo("e-mail")}</p></address></div>
</div>
<div class="legal-line"><nav aria-label="Informations légales"><a href="/mentions-legales/">Mentions légales</a> · <a href="/politique-confidentialite/">Politique de confidentialité</a></nav><p>© {datetime.date.today().year} {NAME}. Tous droits réservés.</p></div>
</div></footer>'''

def jsonld(items):
    if not items: return ""
    # Sans domaine configuré, publier uniquement les schémas autonomes
    # qui ne nécessitent pas d’URL absolue (ex. FAQPage). Les breadcrumbs,
    # l’organisation et les pages locales attendent la configuration du domaine.
    safe_items = items if CONF else [i for i in items if i.get("@type") == "FAQPage"]
    return "".join(
        f'<script type="application/ld+json">{json.dumps(i, ensure_ascii=False)}</script>\n'
        for i in safe_items
    )

def org_ld():
    o = {"@context":"https://schema.org","@type":"Organization","name":NAME,"url":absu("/"),"logo":absu(LOGO)}
    o["description"] = "Entreprise de transport en ambulance : transferts hospitaliers, trajets réguliers, rapatriement, événements."
    if CFG["AREAS"]: o["areaServed"] = [{"@type":"City","name":x} for x in CFG["AREAS"]]
    if CFG["PHONE_INTL"]: o["telephone"] = CFG["PHONE_INTL"]
    if CFG["EMAIL"]: o["email"] = CFG["EMAIL"]
    if CFG["CITY"] and CFG["COUNTRY"]:
        a = {"@type":"PostalAddress","addressLocality":CFG["CITY"],"addressCountry":CFG["COUNTRY"]}
        if CFG["ADDRESS"]: a["streetAddress"] = CFG["ADDRESS"]
        if CFG["POSTAL"]: a["postalCode"] = CFG["POSTAL"]
        o["address"] = a
    return o

def crumb_ld(crumbs):
    items = [{"@type":"ListItem","position":1,"name":"Accueil","item":absu("/")}]
    for i, (l, p) in enumerate(crumbs, 2):
        it = {"@type":"ListItem","position":i,"name":l}
        if p: it["item"] = absu(p)
        items.append(it)
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items}

def crumb_html(crumbs):
    li = '<li><a href="/">Accueil</a></li>' + "".join(
        (f'<li><a href="{p}">{E(l)}</a></li>' if p else f'<li aria-current="page">{E(l)}</li>') for l, p in crumbs)
    return f'<nav class="breadcrumb" aria-label="Fil d’Ariane"><ol>{li}</ol></nav>'

def webpage_ld(path, title, desc):
    """Schéma WebPage de base, avec ancrage vers le site (isPartOf)."""
    wp = {"@context":"https://schema.org","@type":"WebPage","name":title,"description":desc,"inLanguage":"fr",
          "isPartOf":{"@type":"WebSite","name":NAME,"url":absu("/")}}
    if path: wp["url"] = absu(path)
    return wp

def page(path, title, desc, main, crumbs=None, ld=None, og="website", index=True, file=None, extra_css=None, extra_js=None):
    """Écrit une page complète. path = URL (ex. /faq/)."""
    ld = list(ld or [])
    if crumbs: ld.append(crumb_ld(crumbs))
    if CONF: ld.append(webpage_ld(path if path != "/404.html" else "", title, desc))
    robots = ('<meta name="robots" content="index, follow, max-image-preview:large">\n' if (CFG["INDEXABLE"] and index)
              else '<meta name="robots" content="noindex, nofollow">\n')
    canon = (f'<link rel="canonical" href="{E(absu(path))}">\n<meta property="og:url" content="{E(absu(path))}">\n' if CONF
             else '<!-- canonical et og:url : renseigner CFG["DOMAIN"] dans build.py puis relancer -->\n')
    img = (f'<meta property="og:image" content="{E(absu(LOGO))}">\n<meta property="og:image:width" content="1270">\n'
           f'<meta property="og:image:height" content="1124">\n<meta property="og:image:alt" content="Logo {NAME}">\n'
           f'<meta name="twitter:image" content="{E(absu(LOGO))}">\n<meta name="twitter:image:alt" content="Logo {NAME}">\n' if CONF else "")
    geo = f'<meta name="geo.placename" content="{E(CFG["CITY"])}">\n' if CFG["CITY"] else ""
    extra_css_html = "".join(f'<link rel="stylesheet" href="{E(href)}">\n' for href in (extra_css or []))
    extra_js_html = "".join(f'<script src="{E(src)}" defer></script>\n' for src in (extra_js or []))
    doc = f'''<!DOCTYPE html>
<html lang="fr" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#203566">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{robots}{canon}{geo}<meta property="og:type" content="{og}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:locale" content="fr_FR">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
{img}<meta name="twitter:card" content="{"summary_large_image" if CONF else "summary"}">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<link rel="icon" href="{LOGO}" type="image/png">
<link rel="stylesheet" href="/assets/css/style.css">
{extra_css_html}<script>document.documentElement.className="js";</script>
<script src="/assets/js/main.js" defer></script>
<script src="/assets/js/effects.js" defer></script>
{extra_js_html}{jsonld(ld)}</head>
<body>
{header(path)}
<main id="contenu">
{main}
</main>
{footer()}
{fab()}
</body>
</html>
'''
    fp = file or (path.strip("/") + "/index.html" if path != "/" else "index.html")
    full = os.path.join(ROOT, fp)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(doc)

def phero(h1, lead, crumbs):
    return f'<section class="page-hero"><div class="container">{crumb_html(crumbs)}<h1>{h1}</h1><p class="lead">{lead}</p></div><div class="ridge sm" aria-hidden="true"></div></section>'

def ul(items, cls="ticks"): return f'<ul class="{cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
def faq_details(qs): return "".join(f'<details><summary>{E(q)}</summary><div class="answer"><p>{E(a)}</p></div></details>' for q, a in qs)
def areas_html():
    if CFG["AREAS"]: return ul([E(a) for a in CFG["AREAS"]])
    return ul([f'Ville principale : {val("CITY","ville principale")}', f'Communes desservies : {todo("liste des communes réellement desservies")}', f'Régions / zones : {todo("régions ou zones desservies")}'])

def final_cta(title="Une question, un trajet à organiser ?"):
    return f'''<section class="section"><div class="container"><div class="card red cta-band"><h2>{title}</h2>
<p>Décrivez votre besoin en quelques lignes ; l’équipe vous répond pour confirmer ce qui est possible. Évitez de transmettre des informations médicales dans les formulaires.</p>{ctas()}</div></div></section>'''

def form_status(): return '<div class="form-status" role="status" aria-live="polite" hidden></div>'
def demo_note():
    if CFG["FORM_ENDPOINT"]: return ""
    return '<div class="notice warn"><p><strong>Formulaire en mode démonstration.</strong> Il n’est relié à aucun service d’envoi : aucune donnée n’est transmise ni enregistrée. Utilisez les coordonnées de la page <a href="/contact/">Contact</a> pour joindre l’entreprise.</p></div>'
def fld(id_, label, typ="text", req=True, hint="", extra="", ac=""):
    r = ' required' if req else ''
    star = ' <span class="req" aria-hidden="true">*</span>' if req else ' <span class="meta">(facultatif)</span>'
    h = f'<span class="hint" id="{id_}-h">{hint}</span>' if hint else ""
    d = f' aria-describedby="{id_}-h"' if hint else ""
    a = f' autocomplete="{ac}"' if ac else ""
    return f'<div class="field"><label for="{id_}">{label}{star}</label>{h}<input id="{id_}" name="{id_}" type="{typ}"{r}{d}{a} {extra}></div>'
def consent(id_):
    return (f'<div class="field full"><div class="check"><input type="checkbox" id="{id_}" name="{id_}" required>'
            f'<label for="{id_}">J’ai pris connaissance de la <a href="/politique-confidentialite/">politique de confidentialité</a> et j’accepte que ces informations soient utilisées pour traiter ma demande. <span class="req" aria-hidden="true">*</span></label></div></div>')
def form_open(fid):
    ep = f' data-endpoint="{E(CFG["FORM_ENDPOINT"])}"' if CFG["FORM_ENDPOINT"] else ""
    hp = '<div style="position:absolute;left:-9999px" aria-hidden="true"><label>Ne pas remplir<input name="website" tabindex="-1" autocomplete="off"></label></div>' if CFG["FORM_ENDPOINT"] else ""
    return f'<form class="form" id="{fid}" data-form method="post"{ep}>{hp}'
NOJS = '<noscript><p class="notice warn">Ce formulaire nécessite JavaScript. Utilisez la page <a href="/contact/">Contact</a> pour joindre l’entreprise.</p></noscript>'
WARN_FREE = '<p class="meta">Ne saisissez ni diagnostic, ni information de santé, ni numéro d’assuré dans ce champ.</p>'

def quote_form():
    opts = '<option value="">Choisir…</option>' + "".join(f'<option>{E(s["name"])}</option>' for s in SERVICES) + '<option>Je ne sais pas encore</option>'
    return f'''{demo_note()}{NOJS}{form_open("form-devis")}<div class="form-grid two">
{fld("nom","Nom et prénom",ac="name")}{fld("tel","Téléphone","tel",ac="tel",extra='pattern="[0-9+\\s.\\-]{6,}"')}
{fld("email","E-mail","email",req=False,ac="email")}{fld("date","Date souhaitée","date")}
{fld("depart","Adresse de départ",hint="Ville et quartier suffisent dans un premier temps.")}{fld("destination","Destination",hint="Établissement ou adresse d’arrivée.")}
<div class="field full"><label for="type">Type de transport <span class="req" aria-hidden="true">*</span></label><select id="type" name="type" required>{opts}</select></div>
<div class="field full"><div class="check"><input type="checkbox" id="rappel" name="rappel"><label for="rappel">Je souhaite être rappelé(e).</label></div></div>
<div class="field full"><label for="precisions">Précisions logistiques <span class="meta">(facultatif)</span></label><span class="hint" id="precisions-h">Accès, étage, horaires… Ne saisissez aucune information médicale.</span><textarea id="precisions" name="precisions" aria-describedby="precisions-h"></textarea></div>
{consent("consent-devis")}</div>{WARN_FREE}<div class="btn-row"><button class="btn btn-primary" type="submit">Envoyer la demande de devis</button></div>{form_status()}</form>'''

def contact_form():
    return f'''{demo_note()}{NOJS}{form_open("form-contact")}<div class="form-grid two">
{fld("c-nom","Nom et prénom",ac="name")}{fld("c-tel","Téléphone","tel",ac="tel",extra='pattern="[0-9+\\s.\\-]{6,}"')}
{fld("c-email","E-mail","email",req=False,ac="email")}{fld("c-sujet","Objet de votre message")}
<div class="field full"><label for="c-message">Message <span class="req" aria-hidden="true">*</span></label><span class="hint" id="c-message-h">Décrivez votre demande logistique. Aucune information médicale, s’il vous plaît.</span><textarea id="c-message" name="message" required aria-describedby="c-message-h"></textarea></div>
{consent("consent-contact")}</div><div class="btn-row"><button class="btn btn-primary" type="submit">Envoyer le message</button></div>{form_status()}</form>'''

def map_box():
    if CFG["MAPS_EMBED"]:
        return f'''<div class="map-box" data-map-src="{E(CFG["MAPS_EMBED"])}"><div><p><strong>Carte interactive</strong></p><p class="meta">Le chargement de la carte transmet des données à un service externe (voir la politique de confidentialité). Elle ne se charge qu’après votre accord.</p><button class="btn btn-secondary" type="button" data-map-load>Afficher la carte</button></div></div>'''
    return f'<div class="map-box"><div><p><strong>Emplacement de la carte</strong></p><p class="meta">{todo("lien ou intégration de carte, après choix de la configuration de confidentialité")}</p></div></div>'
def map_text():
    link = f'<a href="{E(CFG["MAPS_LINK"])}" rel="noopener" target="_blank">Ouvrir dans Google Maps (nouvel onglet)</a>' if CFG["MAPS_LINK"] else todo("lien Google Maps")
    return f'<p><strong>Alternative textuelle à la carte :</strong> {NAME} est située à {val("ADDRESS","adresse")}, {val("POSTAL","code postal")} {val("CITY","ville")}. Zones desservies : voir la liste ci-dessus. {link}</p>'

def badges_html():
    items = [f'<li><strong>{len(SERVICES)}</strong> prestations</li>']
    if CFG["AREAS"]: items.append(f'<li><strong>{len(CFG["AREAS"])}</strong> villes desservies</li>')
    items.append('<li><strong>Devis</strong> personnalisé</li>')
    return '<ul class="badges">' + "".join(items) + '</ul>'
def chips_html():
    if CFG["AREAS"]: return '<ul class="chips">' + "".join(f"<li>{E(a)}</li>" for a in CFG["AREAS"]) + '</ul>'
    return areas_html()
def fab():
    href = f'tel:{E(CFG["PHONE_INTL"])}' if CFG["PHONE_INTL"] else "/contact/"
    def ic(d): return '<svg viewBox="0 0 24 24" aria-hidden="true">' + d + '</svg>'
    phone = ic('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>')
    doc = ic('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>')
    up = ic('<path d="M12 19V5M5 12l7-7 7 7"/>')
    return (f'<div class="fab"><button class="fab-top" type="button" aria-label="Retour en haut de page">{up}</button>'
            f'<a class="fab-quote" href="/tarifs-devis/" aria-label="Demander un devis">{doc}<span>Devis</span></a>'
            f'<a class="fab-call" href="{href}" aria-label="Appeler">{phone}<span>Appeler</span></a></div>')

# ───────────── PAGES ─────────────
# ───────────── ACCUEIL : contenu enrichi ─────────────
ICONS = {
 "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
 "route": '<circle cx="6" cy="19" r="3"/><path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15"/><circle cx="18" cy="5" r="3"/>',
 "clipboard": '<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1"/>',
 "lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
}
def ico(name): return f'<span class="ico"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg></span>'

FAQD = dict(FAQ_FLAT)
HOME_FAQ = [(q, FAQD[q]) for q in [
 "Comment faire une demande de transport ?",
 "Comment obtenir un devis ?",
 "Quel délai prévoir avant un transport programmé ?",
 "Les demandes sont-elles possibles la nuit et le week-end ?",
 "Dois-je envoyer des informations médicales ?",
 "Une prise en charge ou un remboursement est-il possible ?",
 "Quelle différence entre fauteuil roulant, transport sanitaire et transport médicalisé ?",
 "TAMUDA INJAD est-elle un service d’urgence ?",
]]

SERVICE_TABLE = {
 "ambulance-24h-24": ("Transport demandé en dehors des horaires de bureau", "Adresse, destination, heure souhaitée"),
 "transport-medicalise": ("Surveillance indiquée par un professionnel de santé", "Demande de l’établissement, coordonnées des services"),
 "transfert-hospitalier": ("Passage d’un établissement à un autre ou retour à domicile", "Établissements, services, heure de sortie"),
 "patient-alite-fauteuil-roulant": ("Mobilité réduite : personne allongée ou en fauteuil", "Type de fauteuil, accès, étage, ascenseur"),
 "dialyse-chimiotherapie": ("Séances régulières vers un centre de soins", "Calendrier des séances, lieu, horaires"),
 "rapatriement-sanitaire": ("Retour depuis un lieu éloigné", "Lieu actuel, destination, assurance éventuelle"),
 "ambulance-evenementielle": ("Présence d’une ambulance lors d’un événement", "Date, lieu, nombre de participants"),
}
REG_NORD = "Tanger-Tétouan-Al Hoceïma"
AREA_INFO = {
 "Tétouan": (REG_NORD, "Zone locale"), "Martil": (REG_NORD, "Zone locale"), "M’diq": (REG_NORD, "Zone locale"),
 "Chefchaouen": (REG_NORD, "Zone locale"), "Tanger": (REG_NORD, "Zone locale"), "Fahs-Anjra": (REG_NORD, "Zone locale"),
 "Rabat": ("Rabat-Salé-Kénitra", "Transfert sur demande"), "Casablanca": ("Casablanca-Settat", "Transfert sur demande"),
}

HOME_TITLE = (f"Ambulance à {CFG['CITY']} – Transport sanitaire | {NAME}" if CFG["CITY"] else f"{NAME} – Transport en ambulance")
HOME_DESC = (f"{NAME} : transport en ambulance à {CFG['CITY']} et dans sa région. Sept prestations, transferts hospitaliers, trajets réguliers, devis sur demande."
             if CFG["CITY"] else "Entreprise de transport en ambulance : sept prestations, transferts hospitaliers, trajets réguliers, devis sur demande.")

def home_ld():
    if not CONF: return []
    biz = org_ld()
    biz.update({"@type": "LocalBusiness", "@id": absu("/#entreprise"), "description": HOME_DESC, "image": absu(LOGO),
        "areaServed": [{"@type": "City", "name": a} for a in CFG["AREAS"]],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Services de transport en ambulance",
            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "description": s["short"], "url": absu(f"/services/{s['slug']}/")}} for s in SERVICES]}})
    site = {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": absu("/"), "inLanguage": "fr"}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in HOME_FAQ]}
    return [biz, site, faq]

def build_home():
    cards = "".join(f'<a class="card link-card" href="/services/{s["slug"]}/"><span class="num">{i:02d}</span><h3>{E(s["name"])}</h3><p>{E(s["short"])}</p><span class="more">En savoir plus →</span></a>' for i, s in enumerate(SERVICES, 1))
    # Chiffres clés (uniquement des faits vérifiables dans le site)
    stats = [(str(len(SERVICES)), "prestations de transport en ambulance")]
    if CFG["AREAS"]: stats.append((str(len(CFG["AREAS"])), "villes et zones desservies"))
    stats += [("4", "étapes pour organiser un trajet"), ("Devis", "personnalisé selon votre trajet")]
    stats_html = '<div class="stats">' + "".join(f'<div class="stat"><strong>{n}</strong><span>{E(l)}</span></div>' for n, l in stats) + '</div>'
    # Tableau d'orientation
    def svc(sl): return f'<a href="/services/{sl}/">{E(SBY[sl]["name"])}</a>'
    choose = [
        ("Mobilité réduite : rendez-vous ou retour à domicile", "patient-alite-fauteuil-roulant", "Type de fauteuil, étage, ascenseur, largeur des accès"),
        ("Passage d’un établissement de santé à un autre", "transfert-hospitalier", "Établissements et services, heure de sortie, contact joignable"),
        ("Séances régulières dans un centre de soins", "dialyse-chimiotherapie", "Calendrier des séances, adresse du centre, point de prise en charge"),
        ("Surveillance indiquée par un professionnel de santé", "transport-medicalise", "Demande de l’établissement, transmise par un canal sécurisé"),
        ("Demande en dehors des horaires habituels", "ambulance-24h-24", "Adresse précise, personne joignable (disponibilité à confirmer)"),
        ("Retour depuis un lieu éloigné", "rapatriement-sanitaire", "Lieu actuel, destination, assurance ou assistance éventuelle"),
        ("Présence sur un événement", "ambulance-evenementielle", "Date, lieu, nombre de participants, plan d’accès"),
    ]
    choose_rows = "".join(f'<tr><th scope="row">{E(a)}</th><td>{svc(b)}</td><td>{E(c)}</td></tr>' for a, b, c in choose)
    why = [("Informations claires", "Chaque étape de la demande est expliquée : zone, horaire, interlocuteur."),
           ("Coordination", "Échanges avec les familles et les établissements pour organiser le trajet."),
           ("Devis personnalisé", "Établi à partir du trajet, de la date et du type de transport. Aucun prix n’est affiché sans devis."),
           ("Données protégées", "Aucune information médicale n’est demandée dans les formulaires du site.")]
    why_html = "".join(f'<div class="card"><span class="num" aria-hidden="true">✓</span><h3>{E(t)}</h3><p>{E(d)}</p></div>' for t, d in why)
    eng = ul([f"Réponse aux demandes : {todo('délai à confirmer')}", f"Horaires d’intervention : {todo('à confirmer')}", f"Agréments et autorisations : {todo('à vérifier avant publication')}"])
    steps = [("Vous nous contactez", "Par téléphone ou via le formulaire de devis : départ, destination, date et type de transport."), ("Nous étudions la demande", "Vérification de la faisabilité, de la zone et des disponibilités."), ("Vous recevez une confirmation", "Horaire, interlocuteur et modalités vous sont précisés."), ("Le trajet est réalisé", "Prise en charge au lieu convenu et remise à destination.")]
    st = '<ol class="steps">' + "".join(f"<li><h3>{a}</h3><p>{b}</p></li>" for a, b in steps) + "</ol>"
    def tog(q, inner): return f'<details><summary>{E(q)}</summary><div class="answer">{inner}</div></details>'
    prep = (tog("Pour le trajet", ul(["Adresse ou ville de départ et destination.", "Date et heure souhaitées, avec une éventuelle souplesse.", "Nom et numéro d’une personne joignable."]))
          + tog("Pour l’accès au lieu de prise en charge", ul(["Étage, ascenseur, marches éventuelles.", "Code d’accès ou point de rendez-vous.", "Mobilité : allongé, assis, fauteuil manuel ou électrique."]))
          + tog("Pour des trajets réguliers", ul(["Calendrier et horaires des séances.", "Adresse du centre et point de prise en charge.", "Interlocuteur à prévenir en cas de changement."]))
          + tog("Ce qu’il ne faut pas envoyer en ligne", "<p>Aucun diagnostic, dossier médical ni numéro d’assuré dans les formulaires. L’entreprise vous indiquera par quel canal transmettre un document si nécessaire.</p>"))
    zone_rows = ('<tr><th scope="row">Tétouan et sa région</th><td>Tétouan, Martil, M’diq, Chefchaouen, Tanger, Fahs-Anjra</td><td>Transports organisés, à confirmer pour chaque trajet</td></tr>'
                 '<tr><th scope="row">Transferts longue distance</th><td>Rabat, Casablanca et d’autres destinations</td><td>Sur demande, après étude de faisabilité</td></tr>')
    blog = "".join(f'<a class="card link-card" href="/blog/{a["slug"]}/"><h3>{E(a["title"])}</h3><p>{E(a["desc"])}</p><span class="more">Lire l’article →</span></a>' for a in ARTICLES)
    faq_items = [FAQ_FLAT[i] for i in (0, 1, 5, 6, 7, 10, 19, 20)]
    main = f'''<section class="hero"><div class="container"><div>
<span class="eyebrow">Transport en ambulance</span>
<h1>Transport en ambulance à Tétouan et dans sa région</h1>
<p class="lead">{NAME} organise vos transports en ambulance à Tétouan, Martil, M’diq, Chefchaouen, Tanger et Fahs-Anjra, ainsi que vos transferts vers Rabat, Casablanca et d’autres destinations sur demande.</p>
{ctas()}{badges_html()}</div>
<div class="hero-logo"><img src="{LOGO}" width="300" height="266" fetchpriority="high" decoding="async" alt="Logo {NAME} : une ambulance sur une route de montagne"></div></div><div class="ridge" aria-hidden="true"></div></section>
<section class="section stats-wrap" aria-label="Chiffres clés"><div class="container">{stats_html}</div></section>
<section class="section" aria-labelledby="h-services"><div class="container"><span class="eyebrow">Nos prestations</span><h2 id="h-services">Sept services de transport en ambulance</h2>
<p class="lead">Chaque prestation a ses spécificités. Choisissez celle qui ressemble le plus à votre situation ou <a href="/services/">consultez notre guide d’orientation</a>.</p>
<div class="grid cols-3" style="margin-top:1.5rem">{cards}</div></div></section>
<section class="section soft" aria-labelledby="h-choisir"><div class="container"><span class="eyebrow">Orientation</span><h2 id="h-choisir">Quel transport pour quelle situation ?</h2>
<p class="lead">Un repère pratique, pas un avis médical : seul un professionnel de santé peut indiquer le type de transport adapté.</p>
<div class="table-wrap" role="region" aria-labelledby="cap-choisir" tabindex="0"><table><caption id="cap-choisir">Situations courantes, prestation correspondante et informations à préparer</caption>
<thead><tr><th scope="col">Situation</th><th scope="col">Prestation</th><th scope="col">À préparer</th></tr></thead><tbody>{choose_rows}</tbody></table></div></div></section>
<section class="section" aria-labelledby="h-engagements"><div class="container"><div class="two-col"><div><span class="eyebrow">L’entreprise</span><h2 id="h-engagements">{NAME}, entreprise de transport en ambulance</h2>
<p>{NAME} organise des trajets en coordination avec les familles et les établissements, avec des informations claires à chaque étape. <a href="/a-propos/">Découvrir l’entreprise</a>.</p>
<div class="notice warn"><p><strong>À confirmer avant publication :</strong></p>{eng}</div></div>
<div class="grid" style="align-content:start">{why_html}</div></div></div></section>
<section class="section soft" aria-labelledby="h-etapes"><div class="container two-col"><div><span class="eyebrow">Déroulement</span><h2 id="h-etapes">Les étapes d’une demande de transport</h2>{st}</div>
<div><span class="eyebrow">Préparer sa demande</span><h2>Les informations utiles</h2><p>Quelques informations logistiques suffisent pour étudier votre demande.</p>{prep}</div></div></section>
<section class="section" aria-labelledby="h-zone"><div class="container"><span class="eyebrow">Zone d’intervention</span><h2 id="h-zone">Ambulance à Tétouan, Martil, M’diq, Tanger et Chefchaouen</h2>
{chips_html()}<p class="lead">Les zones sont à confirmer pour chaque trajet : l’équipe vérifie la faisabilité avant de s’engager.</p>
<div class="table-wrap" role="region" aria-labelledby="cap-zone" tabindex="0"><table><caption id="cap-zone">Zones desservies et modalités</caption>
<thead><tr><th scope="col">Zone</th><th scope="col">Villes</th><th scope="col">Modalités</th></tr></thead><tbody>{zone_rows}</tbody></table></div>
<p style="margin-top:1rem"><a href="/zone-intervention/">Voir la page Zone &amp; carte</a></p></div></section>
<section class="section soft" aria-labelledby="h-blog"><div class="container"><span class="eyebrow">Conseils pratiques</span><h2 id="h-blog">Préparer un transport : nos articles</h2>
<div class="grid cols-3" style="margin-top:1.5rem">{blog}</div><p style="margin-top:1.25rem"><a href="/blog/">Tous les articles du blog</a></p></div></section>
<section class="section" aria-labelledby="h-faq"><div class="container prose"><span class="eyebrow">FAQ</span><h2 id="h-faq">Questions fréquentes sur le transport en ambulance</h2>{faq_details(faq_items)}<p><a href="/faq/">Voir les {len(FAQ_FLAT)} questions de la FAQ</a></p></div></section>
{testi_carousel(home=True)}
{final_cta("Parlons de votre trajet")}'''
    ld = [org_ld(), {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": absu("/"), "inLanguage": "fr"},
          {"@context": "https://schema.org", "@type": "ItemList", "name": "Prestations de transport en ambulance",
           "itemListElement": [{"@type": "ListItem", "position": i, "name": s["name"], "url": absu(f"/services/{s['slug']}/")} for i, s in enumerate(SERVICES, 1)]},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_items]}]
    page("/", f"Ambulance à {CFG['CITY']} et région : {len(SERVICES)} prestations | {NAME}",
         f"Transport en ambulance à {CFG['CITY']}, Martil, M’diq, Chefchaouen et Tanger : transferts hospitaliers, dialyse, fauteuil roulant, rapatriement. Devis sur demande.",
         main, ld=ld, **t_assets())

def build_services():
    cards = "".join(f'<a class="card link-card" href="/services/{s["slug"]}/"><h2 style="font-size:1.25rem">{E(s["name"])}</h2><p>{E(s["short"])}</p><span class="more">Voir la prestation →</span></a>' for s in SERVICES)
    guide = ul(["<strong>Un rendez-vous ou un retour à domicile, avec une mobilité réduite ?</strong> Voir <a href=\"/services/patient-alite-fauteuil-roulant/\">Patient alité / fauteuil roulant</a>.",
        "<strong>Un passage d’un établissement à un autre ?</strong> Voir <a href=\"/services/transfert-hospitalier/\">Transfert hospitalier</a>.",
        "<strong>Des séances régulières ?</strong> Voir <a href=\"/services/dialyse-chimiotherapie/\">Dialyse &amp; chimiothérapie</a>.",
        "<strong>Un événement à couvrir ?</strong> Voir <a href=\"/services/ambulance-evenementielle/\">Ambulance événementielle</a>.",
        "<strong>Une surveillance médicale indiquée par un professionnel ?</strong> Voir <a href=\"/services/transport-medicalise/\">Transport médicalisé</a>.",
        "<strong>Un retour depuis un lieu éloigné ?</strong> Voir <a href=\"/services/rapatriement-sanitaire/\">Rapatriement sanitaire</a>."])
    cr = [("Services", None)]
    main = phero("Nos services de transport en ambulance", "Sept prestations pour des besoins différents. Trouvez celle qui correspond à votre situation, puis préparez votre demande.", cr) + f'''
<section class="section"><div class="container"><div class="grid cols-3">{cards}</div></div></section>
<section class="section soft"><div class="container prose"><h2>Comment s’orienter ?</h2>
<p>Ce guide est une aide à la lecture du site, pas un avis médical : seul un professionnel de santé peut dire quel type de transport convient à une situation.</p>{guide}
<div class="notice info"><p>Cette orientation ne constitue ni un diagnostic, ni un conseil médical personnalisé.</p></div>{ctas()}</div></section>
{final_cta("Un doute sur la prestation adaptée ?")}'''
    page("/services/", f"Services de transport en ambulance | {NAME}", "Découvrez les sept prestations de TAMUDA INJAD : ambulance 24h/24, transport médicalisé, transfert hospitalier, fauteuil roulant, dialyse, rapatriement, événementiel.", main, cr)

def build_service(s):
    path = f"/services/{s['slug']}/"
    cr = [("Services", "/services/"), (s["name"], None)]
    notice = f'<div class="notice warn"><p><strong>À confirmer avant publication.</strong> {s["notice"]}</p></div>' if s.get("notice") and not (s["slug"] == "ambulance-24h-24" and CFG["AVAIL_24H"]) else ""
    brief = [("En résumé", E(s["short"])),
             ("À préparer", "Les informations logistiques listées plus bas suffisent pour une première demande : rien de plus n’est exigé à ce stade."),
             ("Zone et devis", "L’équipe confirme la faisabilité pour votre adresse, puis établit un devis : voir la page <a href=\"/tarifs-devis/\">Tarifs &amp; devis</a>.")]
    brief_html = '<div class="grid cols-3" style="margin:1.5rem 0">' + "".join(
        f'<div class="card"><span class="num" aria-hidden="true">{i}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(brief, 1)) + '</div>'
    steps = '<ol class="steps">' + "".join(f"<li><h3>{a}</h3><p>{b}</p></li>" for a, b in s["orga"]) + "</ol>"
    rel = "".join(f'<a class="card link-card" href="/services/{r}/"><h3>{E(SBY[r]["name"])}</h3><p>{E(SBY[r]["short"])}</p></a>' for r in s["rel"])
    eq = eq_note("") if s.get("eq") else eq_note("Aucun équipement ni accompagnement n’est annoncé tant qu’il n’est pas confirmé. ")
    main = phero(E(s["h1"]), E(s["intro"]), cr) + f'''
<section class="section"><div class="container two-col wide-left"><div class="prose">
{notice}{brief_html}
<h2>Présentation et périmètre</h2><p>{E(s["scope"])}</p>
<h2>Situations concernées</h2>{ul([E(x) for x in s["situations"]])}
<h2>Organisation du transport</h2>{steps}
<h2>Informations à préparer</h2>{ul([E(x) for x in s["prep"]])}
<h2>Équipements et accompagnement</h2>{eq}
<h2>Zone d’intervention</h2>{areas_html()}<p>Détail sur la page <a href="/zone-intervention/">Zone &amp; carte</a>.</p>
<h2>Tarifs et devis</h2><p>Le prix dépend de la situation (trajet, horaires, type de transport). Aucun tarif n’est affiché ici : <a href="/tarifs-devis/">consultez la page Tarifs &amp; devis</a> pour demander un devis.</p>
<h2>Questions fréquentes sur ce service</h2>{faq_details(s["faq"])}
</div><aside><div class="card red"><h2 style="font-size:1.3rem">Besoin de ce service ?</h2><p>Appelez-nous ou demandez un devis.</p>{ctas()}</div>
<div class="notice"><p><strong>Urgence vitale ?</strong> Contactez immédiatement les secours compétents. {NAME} n’est pas un service d’urgence.</p></div>
<div class="card"><h2 style="font-size:1.1rem">Sur le même thème</h2><ul class="ticks"><li><a href="/blog/preparer-un-transport-en-ambulance/">Préparer un transport : la checklist</a></li><li><a href="/blog/informations-pour-un-devis-de-transport/">Informations pour un devis</a></li><li><a href="/faq/">La FAQ complète</a></li></ul></div></aside></div></section>
<section class="section soft"><div class="container"><h2>Prestations liées</h2><div class="grid cols-3">{rel}</div></div></section>
{final_cta()}'''
    svc = {"@context":"https://schema.org","@type":"Service","name":s["name"],"serviceType":s["name"],"description":s["short"],"url":absu(path),
           "provider":{"@type":"LocalBusiness","name":NAME,"url":absu("/")}}
    if CFG["AREAS"]: svc["areaServed"] = [{"@type":"City","name":x} for x in CFG["AREAS"]]
    fq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in s["faq"]]}
    page(path, f"{s['name']} | {NAME}", s["short"], main, cr, [svc, fq])

def build_zone():
    cr = [("Zone & carte", None)]
    # Villes locales (affichées dans la liste interactive + markers)
    LOCAL_CITIES = [
        ("tetouan", "Tétouan"),
        ("martil", "Martil"),
        ("mdiq", "M’diq"),
        ("cabo-negro", "Cabo Negro"),
        ("fnideq", "Fnideq"),
        ("tanger", "Tanger"),
        ("fahs-anjra", "Fahs-Anjra"),
        ("chefchaouen", "Chefchaouen"),
    ]
    city_btns = "".join(
        f'<li><button type="button" class="zone-city-btn" data-city="{cid}" aria-pressed="false">'
        f'<span class="pin-dot" aria-hidden="true"></span>{E(name)}'
        f'<span class="tag-mini">Locale</span></button></li>'
        for cid, name in LOCAL_CITIES
    )
    zone_rows = "".join(f'<tr><th scope="row">{E(v)}</th><td>{E(r)}</td><td>{E(t)}</td></tr>' for v, (r, t) in AREA_INFO.items())
    n_local = sum(1 for _, (_, t) in AREA_INFO.items() if t == "Zone locale")
    stats = [(str(len(CFG["AREAS"])), "villes et zones listées"),
             (str(n_local), "villes en zone locale"),
             ("1", "vérification avant chaque trajet")]
    stats_html = '<div class="stats">' + "".join(f'<div class="stat"><strong>{n}</strong><span>{E(l)}</span></div>' for n, l in stats) + '</div>'
    routes = [
        ("Tétouan", "Martil", "local"),
        ("Tétouan", "M’diq", "local"),
        ("Tétouan", "Chefchaouen", "local"),
        ("Tétouan", "Tanger", "local"),
        ("Tétouan", "Rabat", "demand"),
        ("Tétouan", "Casablanca", "demand"),
    ]
    route_cards = "".join(
        f'<li><a class="card link-card route-card" href="/tarifs-devis/">'
        f'<span class="route">{E(a)} <span aria-hidden="true">→</span><span class="sr-only">vers</span> {E(b)}</span>'
        f'<span class="tag {"local" if kind=="local" else "demand"}">{"Zone locale" if kind=="local" else "Sur demande"}</span>'
        f'<span class="more">Demander un devis →</span></a></li>'
        for a, b, kind in routes
    )
    csteps = [("Vous indiquez un départ et une arrivée", "Villes ou adresses, avec l’heure souhaitée."),
              ("L’équipe vérifie la faisabilité", "Distance, zone, accès aux lieux et disponibilités."),
              ("Vous recevez une confirmation", "Horaire, modalités et devis si demandé."),
              ("Le trajet est organisé", "Prise en charge au lieu convenu, puis remise à destination.")]
    st = '<ol class="steps">' + "".join(f"<li><h3>{a}</h3><p>{b}</p></li>" for a, b in csteps) + "</ol>"
    def tog(q, inner): return f'<details><summary>{E(q)}</summary><div class="answer">{inner}</div></details>'
    toggles = (tog("Ma commune n’apparaît pas dans la liste : puis-je quand même demander un trajet ?",
                   "<p>Oui. La liste présente les zones déjà étudiées, elle n’est pas exhaustive. Décrivez votre trajet (départ, arrivée, date) : l’équipe vous répondra pour confirmer si celui-ci peut être assuré.</p>")
             + tog("La liste garantit-elle qu’un trajet sera accepté ?",
                   "<p>Non. Être dans une zone listée ne vaut pas confirmation : la faisabilité dépend du véhicule, des disponibilités et des accès au moment de votre demande.</p>")
             + tog("Comment savoir si mon adresse est accessible ?",
                   "<p>Indiquez lors de la demande les éléments d’accès : étage, ascenseur, marches, largeur des portes, distance au stationnement.</p>")
             + tog("La carte utilise-t-elle un service externe ?",
                   "<p>Oui. La carte est fournie par OpenStreetMap / Leaflet. Son affichage peut transmettre votre adresse IP au fournisseur de tuiles. L’alternative textuelle (liste des villes) reste toujours disponible.</p>"))
    cards_links = (f'<a class="card link-card" href="/services/"><h3>Nos services</h3><p>Les sept prestations de transport en ambulance et leurs modalités.</p><span class="more">Voir les services →</span></a>'
                   f'<a class="card link-card" href="/tarifs-devis/"><h3>Tarifs &amp; devis</h3><p>Les informations utiles pour obtenir un devis de votre trajet.</p><span class="more">Demander un devis →</span></a>'
                   f'<a class="card link-card" href="/contact/"><h3>Contact</h3><p>Téléphone, e-mail et formulaire pour joindre l’équipe.</p><span class="more">Nous contacter →</span></a>')
    # Bloc carte interactive (Leaflet après consentement)
    map_block = f'''
<div class="zone-hero-map" id="zone-map-root">
  <div class="zone-map-panel">
    <div id="zone-map" role="img" aria-label="Carte interactive des villes desservies autour de Tétouan"></div>
    <div class="zone-map-placeholder" id="zone-map-placeholder">
      <p><strong>Chargement de la carte…</strong></p>
      <p class="meta">OpenStreetMap · Tétouan et zone locale</p>
    </div>
  </div>
  <div class="zone-cities-panel">
    <div class="zone-cities-head">
      <h2>Villes de la zone locale</h2>
      <p>Sélectionnez une ville pour la repérer sur la carte.</p>
    </div>
    <ul class="zone-cities-list" aria-label="Villes de la zone locale">{city_btns}</ul>
    <div class="zone-cities-foot">Cliquez une ville pour centrer la carte · zone indicative, chaque trajet est confirmé.</div>
  </div>
</div>
<div class="zone-legend-bar" aria-label="Légende de la carte">
  <span class="leg"><span class="dot local" aria-hidden="true"></span> Ville zone locale</span>
  <span class="leg"><span class="dot circle" aria-hidden="true"></span> Périmètre indicatif (~28 km)</span>
  <span class="leg"><span class="dot demand" aria-hidden="true"></span> Transfert sur demande (hors carte)</span>
</div>
<p class="meta" style="margin-top:.75rem"><strong>Adresse :</strong> {NAME}, {val("ADDRESS","adresse")}, {val("POSTAL","code postal")} {val("CITY","ville")}.
{f'<a href="{E(CFG["MAPS_LINK"])}" rel="noopener" target="_blank">Ouvrir dans Google Maps</a>' if CFG["MAPS_LINK"] else todo("lien Google Maps")}</p>
'''
    main = phero(
        "Zone d’intervention : ambulance à Tétouan et dans le nord du Maroc",
        f"{NAME} organise des transports en ambulance à Tétouan, Martil, M’diq, Chefchaouen, Tanger et Fahs-Anjra, et des transferts vers Rabat et Casablanca sur demande. Chaque trajet est confirmé par l’équipe avant le départ.",
        cr
    ) + f'''
<section class="section" aria-labelledby="h-carte">
  <div class="container">
    <span class="eyebrow">Carte des zones</span>
    <h2 id="h-carte">Les villes desservies en un coup d’œil</h2>
    {map_block}
  </div>
</section>

<section class="section soft stats-wrap" aria-label="Chiffres clés"><div class="container">{stats_html}</div></section>

<section class="section" aria-labelledby="h-trajets">
  <div class="container">
    <span class="eyebrow">Trajets types</span>
    <h2 id="h-trajets">Les trajets les plus demandés</h2>
    <p class="lead">Exemples de liaisons étudiées au départ de Tétouan. Chaque trajet reste à confirmer selon l’adresse, l’horaire et la disponibilité du véhicule.</p>
    <ul class="route-grid">{route_cards}</ul>
    <p class="meta" style="margin-top:1rem">Autre départ ou destination ? Utilisez le vérificateur ci-dessous. Besoin d’un type de transport précis ? Consultez nos <a href="/services/">services</a>.</p>
  </div>
</section>

<section class="section soft" aria-labelledby="h-table-zones">
  <div class="container">
    <span class="eyebrow">Détail</span>
    <h2 id="h-table-zones">Villes et modalités d’intervention</h2>
    <div class="table-wrap" role="region" aria-labelledby="cap-zones" tabindex="0">
      <table>
        <caption id="cap-zones">Villes desservies, région et modalités</caption>
        <thead><tr><th scope="col">Ville</th><th scope="col">Région</th><th scope="col">Modalités</th></tr></thead>
        <tbody>{zone_rows}</tbody>
      </table>
    </div>
    <div class="notice info" style="margin-top:1.25rem"><p>Cette liste n’est pas exhaustive. Être dans une zone listée ne vaut pas confirmation automatique : l’équipe vérifie chaque trajet.</p></div>
  </div>
</section>

<section class="section" aria-labelledby="h-verifier">
  <div class="container two-col wide-left">
    <div>
      <span class="eyebrow">Vérifier un trajet</span>
      <h2 id="h-verifier">Indiquez un départ et une arrivée</h2>
      <p>Saisissez deux villes pour voir dans quelle catégorie entre votre trajet, puis envoyez votre demande : l’équipe vous répond pour confirmer.</p>
      {demo_note()}{NOJS}
      {form_open("form-zone")}
      <div class="form-grid two">
        {fld("z-depart","Adresse ou ville de départ",hint="Ex. Tétouan, Martil…",extra='list="zone-cities"')}
        {fld("z-arrivee","Adresse ou ville d’arrivée",hint="Ex. M’diq, Rabat…",extra='list="zone-cities"')}
        {fld("z-tel","Téléphone","tel",ac="tel",extra='pattern="[0-9+\\s.\\-]{6,}"')}
      </div>
      <datalist id="zone-cities">
        <option value="Tétouan"><option value="Martil"><option value="M’diq"><option value="Chefchaouen">
        <option value="Tanger"><option value="Fahs-Anjra"><option value="Cabo Negro"><option value="Fnideq">
        <option value="Rabat"><option value="Casablanca">
      </datalist>
      <p class="route-result" id="route-result" role="status" aria-live="polite" hidden></p>
      {consent("consent-zone")}
      <div class="btn-row"><button class="btn btn-primary" type="submit">Préparer ma demande</button></div>
      {form_status()}
      </form>
    </div>
    <aside>
      <span class="eyebrow">Déroulement</span>
      <h2 style="font-size:1.4rem">De la demande au trajet</h2>
      {st}
    </aside>
  </div>
</section>

<section class="section soft" aria-labelledby="h-faq-zone">
  <div class="container prose">
    <span class="eyebrow">FAQ zone</span>
    <h2 id="h-faq-zone">Questions fréquentes sur la zone d’intervention</h2>
    {toggles}
    <p><a href="/faq/">Voir toute la FAQ</a> · <a href="/blog/preparer-un-transport-en-ambulance/">Préparer un transport</a> · <a href="/a-propos/">À propos</a></p>
  </div>
</section>

<section class="section" aria-labelledby="h-zones-liens">
  <div class="container">
    <span class="eyebrow">Pour aller plus loin</span>
    <h2 id="h-zones-liens">Découvrir {NAME}</h2>
    <div class="grid cols-3" style="margin-top:1.5rem">{cards_links}</div>
  </div>
</section>
{final_cta("Votre ville n’apparaît pas ? Demandez-nous")}'''
    fq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in [
            ("Ma commune n’apparaît pas dans la liste : puis-je quand même demander un trajet ?",
             "Oui. La liste présente les zones déjà étudiées, elle n’est pas exhaustive : décrivez votre trajet et l’équipe vous répondra pour confirmer s’il peut être assuré."),
            ("La liste garantit-elle qu’un trajet sera accepté ?",
             "Non. Être dans une zone listée ne vaut pas confirmation : la faisabilité dépend du véhicule, des disponibilités et des accès au moment de la demande."),
            ("Comment savoir si mon adresse est accessible ?",
             "Indiquez les éléments d’accès lors de la demande : étage, ascenseur, marches, largeur des portes, distance au stationnement."),
            ("La carte utilise-t-elle un service externe ?",
             "Oui. La carte est fournie par OpenStreetMap / Leaflet. Son affichage peut transmettre votre adresse IP au fournisseur de tuiles. L’alternative textuelle (liste des villes) reste toujours disponible."),
        ]
    ]}
    page(
        "/zone-intervention/",
        f"Zone d’intervention : ambulance à {CFG['CITY']}, Tanger et Chefchaouen | {NAME}",
        f"Zones desservies par {NAME} : {', '.join(CFG['AREAS'])}. Carte interactive, villes de la zone locale, trajets types et vérification de faisabilité.",
        main, cr, [fq],
        extra_css=["/assets/css/zone.css"],
        extra_js=["/assets/js/zone.js"],
    )

def build_tarifs():
    cr = [("Tarifs & devis", None)]
    el = ul(["Adresse ou ville de départ et destination.","Date et horaire souhaités.","Type de transport (voir la liste des services).","Contraintes d’accès : étage, ascenseur, escaliers.","Présence d’un accompagnant.","Trajet simple, aller-retour ou récurrent."])
    factors = [
        ("Distance et itinéraire", "La longueur du trajet, l’aller-retour éventuel et les conditions de route servent de base au calcul du devis."),
        ("Type de transport", "Personne en fauteuil, transport allongé ou surveillance médicalisée : le véhicule et l’équipe mobilisée ne sont pas les mêmes."),
        ("Horaires et délais", "Nuit, week-end, jour férié ou demande de dernière minute : ces éléments changent l’organisation et peuvent influencer le tarif."),
        ("Accès et accompagnement", "Étage, ascenseur, escaliers, distance de stationnement et présence d’un accompagnant modifient le temps d’intervention."),
    ]
    factors_html = "".join(f'<div class="card"><span class="num" aria-hidden="true">{i:02d}</span><h3>{E(t)}</h3><p>{E(d)}</p></div>' for i, (t, d) in enumerate(factors, 1))
    examples = [
        ("Rendez-vous médical dans la ville", "Transport assis ou en fauteuil roulant", "Adresse, heure du rendez-vous, accès du logement"),
        ("Retour d’hospitalisation à domicile", "Transport allongé ou assis selon la mobilité", "Établissement de sortie, service, heure prévue"),
        ("Transfert entre deux établissements", "Selon l’indication du professionnel de santé", "Établissements et services, contacts, créneau"),
        ("Séance de dialyse ou de chimiothérapie", "Trajet régulier aller-retour", "Calendrier des séances, adresse du centre"),
        ("Présence d’ambulance sur un événement", "Dispositif étudié au cas par cas", "Date, lieu, durée, nombre de participants"),
    ]
    ex_rows = "".join(f'<tr><th scope="row">{E(a)}</th><td>{E(b)}</td><td>{E(c)}</td></tr>' for a, b, c in examples)
    dsteps = [("Vous décrivez le besoin", "Départ, destination, date, type de transport et contraintes d’accès, par formulaire ou par téléphone."),
              ("L’équipe étudie la demande", "Vérification de la faisabilité, de la zone et des disponibilités ; une question peut vous être posée pour préciser un point."),
              ("Vous recevez une proposition", "Un devis précise le prix, les modalités et ce qui est inclus. Aucun engagement n’est pris avant votre accord."),
              ("Vous confirmez le transport", "Après validation, l’horaire et l’interlocuteur vous sont confirmés.")]
    dsteps_html = '<ol class="steps">' + "".join(f"<li><h3>{a}</h3><p>{b}</p></li>" for a, b in dsteps) + "</ol>"
    extra_devis = [
        ("Que se passe-t-il après l’envoi du formulaire ?", "L’équipe reprend contact avec vous pour vérifier les informations et vous proposer un devis. Le délai de réponse est à confirmer avec elle."),
        ("Le devis engage-t-il au transport ?", "Non. Un devis est une proposition : le transport n’est confirmé qu’après votre accord et la validation des disponibilités."),
        ("Puis-je demander plusieurs trajets dans un même devis ?", "Oui, décrivez chaque trajet dans les précisions logistiques (sans aucune information médicale) ; l’entreprise vous répondra pour chaque trajet."),
    ]
    toggles = faq_details(list(FAQ[1][1]) + extra_devis)
    main = phero("Tarifs et demande de devis", "Chaque transport est différent : le tarif est établi à partir du trajet et du type de prestation. Aucun prix n’est publié ici.", cr) + f'''
<section class="section"><div class="container two-col wide-left"><div><h2>Demander un devis</h2>{quote_form()}</div>
<aside><div class="card"><h2 style="font-size:1.3rem">Éléments utiles au devis</h2>{el}</div>
<div class="notice info"><p><strong>Prise en charge et remboursement :</strong> ils dépendent de votre situation et de la réglementation de votre pays. Ce site ne garantit ni ne promet aucune prise en charge.</p></div>
<div class="notice"><p>Merci de ne communiquer ni diagnostic, ni dossier médical dans ce formulaire.</p></div>
<p class="meta">Données traitées pour répondre à votre demande. <a href="/politique-confidentialite/">Politique de confidentialité</a>.</p></aside></div></section>
<section class="section soft" aria-labelledby="h-facteurs"><div class="container"><span class="eyebrow">Transparence</span><h2 id="h-facteurs">Ce qui influence le prix d’un transport</h2>
<p class="lead">Aucun tarif forfaitaire n’est affiché : chaque devis est calculé à partir de ces facteurs, précisés dans la proposition écrite.</p>
<div class="grid cols-2" style="margin-top:1.5rem">{factors_html}</div></div></section>
<section class="section" aria-labelledby="h-exemples"><div class="container"><span class="eyebrow">Exemples</span><h2 id="h-exemples">Situations courantes et éléments pris en compte</h2>
<div class="table-wrap" role="region" aria-labelledby="cap-exemples" tabindex="0"><table><caption id="cap-exemples">Situations de transport, prestation type et informations à préparer</caption>
<thead><tr><th scope="col">Situation</th><th scope="col">Prestation généralement envisagée</th><th scope="col">À préparer</th></tr></thead><tbody>{ex_rows}</tbody></table></div>
<p class="meta" style="margin-top:1rem">Ces exemples sont indicatifs : seule la confirmation de l’entreprise engage ce qui est réalisé.</p></div></section>
<section class="section soft" aria-labelledby="h-deroulement-devis"><div class="container two-col"><div><span class="eyebrow">Déroulement</span><h2 id="h-deroulement-devis">Comment se passe une demande de devis ?</h2>{dsteps_html}</div>
<div><span class="eyebrow">FAQ devis</span><h2>Questions fréquentes sur les devis</h2><p>Les conditions définitives sont toujours confirmées par l’entreprise.</p>{toggles}</div></div></section>
{final_cta("Votre trajet mérite un devis clair")}'''
    fq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in list(FAQ[1][1]) + extra_devis]}
    page("/tarifs-devis/", f"Tarifs et demande de devis | {NAME}", "Demandez un devis de transport en ambulance : facteurs de prix, déroulement de la demande, exemples de situations et formulaire sécurisé.", main, cr, [fq])

def build_faq():
    """Génère une FAQ structurée, accessible et optimisée pour les recherches utiles."""
    cr = [("FAQ", None)]
    category_cards = "".join(
        f'<a class="card link-card faq-category-card" href="#faq-{i}">'
        f'<span class="num">{i:02d}</span><h3>{E(title)}</h3>'
        f'<p>{len(questions)} questions et réponses</p>'
        f'<span class="more">Consulter les réponses →</span></a>'
        for i, (title, questions) in enumerate(FAQ, 1)
    )
    topic_rows = "".join(
        f'<tr><th scope="row"><a href="#faq-{i}">{E(title)}</a></th>'
        f'<td>{len(questions)} questions</td><td>{E(questions[0][0])}</td></tr>'
        for i, (title, questions) in enumerate(FAQ, 1)
    )
    groups = "".join(
        f'<section class="faq-group" id="faq-{i}" aria-labelledby="faq-title-{i}">'
        f'<div class="faq-group-heading"><span class="eyebrow">Rubrique {i:02d}</span>'
        f'<h2 id="faq-title-{i}">{E(title)}</h2>'
        f'<p class="meta">{len(questions)} questions pour vous aider à préparer votre demande.</p></div>'
        f'{faq_details(questions)}'
        f'<p class="faq-back"><a href="#faq-categories">↑ Retour aux rubriques</a></p>'
        f'</section>'
        for i, (title, questions) in enumerate(FAQ, 1)
    )
    fq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in FAQ_FLAT
        ]
    }
    main = phero(
        "FAQ : questions fréquentes sur le transport en ambulance",
        "Retrouvez les réponses aux questions sur la réservation d’une ambulance, les transferts hospitaliers, les devis, les documents à préparer et les trajets réguliers avec TAMUDA INJAD. Les disponibilités et modalités sont à confirmer directement avec l’entreprise.",
        cr
    ) + f'''
<section class="section" aria-labelledby="faq-intro-title">
  <div class="container">
    <div class="two-col wide-left">
      <div class="prose">
        <span class="eyebrow">Centre d’aide TAMUDA INJAD</span>
        <h2 id="faq-intro-title">Comment utiliser cette foire aux questions ?</h2>
        <p>Cette page rassemble les informations pratiques utiles avant de demander un transport en ambulance à Tétouan et dans les zones desservies. Choisissez une rubrique pour consulter les réponses concernant votre situation.</p>
        <p>Les informations qui dépendent des disponibilités, du véhicule, de la réglementation ou de l’organisation de l’entreprise doivent être confirmées au moment de votre demande.</p>
      </div>
      <aside><div class="card red">
        <span class="num" aria-hidden="true">?</span>
        <h2 style="font-size:1.3rem">Vous avez besoin d’une réponse précise ?</h2>
        <p>Notre équipe peut étudier votre demande et vous indiquer les modalités possibles.</p>
        <div class="btn-row">
          <a class="btn btn-primary" href="/contact/">Contacter TAMUDA INJAD</a>
          <a class="btn btn-secondary" href="/tarifs-devis/">Demander un devis</a>
        </div>
      </div></aside>
    </div>
  </div>
</section>
<section class="section soft" id="faq-categories" aria-labelledby="faq-categories-title">
  <div class="container">
    <span class="eyebrow">Navigation rapide</span>
    <h2 id="faq-categories-title">Choisir une rubrique de la FAQ</h2>
    <p class="lead">Accédez directement au sujet qui vous intéresse.</p>
    <div class="grid cols-3" style="margin-top:1.5rem">{category_cards}</div>
  </div>
</section>
<section class="section" aria-labelledby="faq-summary-title">
  <div class="container">
    <span class="eyebrow">Vue d’ensemble</span>
    <h2 id="faq-summary-title">Les thèmes abordés dans notre FAQ ambulance</h2>
    <p class="lead">Un aperçu des informations disponibles avant de réserver un transport ou de demander un devis.</p>
    <div class="table-wrap" role="region" aria-labelledby="faq-table-caption" tabindex="0">
      <table>
        <caption id="faq-table-caption">Rubriques de la FAQ TAMUDA INJAD et exemples de questions</caption>
        <thead><tr><th scope="col">Thème</th><th scope="col">Contenu</th><th scope="col">Exemple de question</th></tr></thead>
        <tbody>{topic_rows}</tbody>
      </table>
    </div>
  </div>
</section>
<section class="section soft" aria-label="Questions et réponses détaillées">
  <div class="container prose">
    <span class="eyebrow">Toutes les réponses</span>
    <h2>Questions fréquentes sur nos services de transport</h2>
    <p>Ouvrez une question pour afficher sa réponse. Les accordéons restent accessibles au clavier et fonctionnent sans JavaScript.</p>
    {groups}
    <div class="notice info">
      <p><strong>Une question reste sans réponse ?</strong> <a href="/contact/">Contactez TAMUDA INJAD</a> en précisant votre besoin logistique. Pour connaître les modalités tarifaires, consultez également la page <a href="/tarifs-devis/">Tarifs et demande de devis</a>.</p>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="faq-related-title">
  <div class="container">
    <span class="eyebrow">Pour aller plus loin</span>
    <h2 id="faq-related-title">Informations utiles sur le transport en ambulance</h2>
    <div class="grid cols-3">
      <a class="card link-card" href="/services/"><h3>Nos services</h3><p>Découvrez les prestations de transport proposées et leurs conditions à confirmer.</p><span class="more">Voir les services →</span></a>
      <a class="card link-card" href="/zone-intervention/"><h3>Zone d’intervention</h3><p>Consultez les villes et les zones pour lesquelles une demande peut être étudiée.</p><span class="more">Voir les zones →</span></a>
      <a class="card link-card" href="/tarifs-devis/"><h3>Tarifs et devis</h3><p>Préparez les informations pratiques nécessaires à l’étude de votre trajet.</p><span class="more">Demander un devis →</span></a>
    </div>
    <div class="notice warn" style="margin-top:1.5rem">
      <p><strong>Important :</strong> TAMUDA INJAD n’est pas un service public d’urgence et cette FAQ ne remplace pas l’avis d’un professionnel de santé. En cas d’urgence vitale, contactez immédiatement les secours compétents de votre pays.</p>
    </div>
  </div>
</section>
{final_cta("Une question sur votre transport ?")}'''
    faq_desc = (
        f"FAQ TAMUDA INJAD : {len(FAQ_FLAT)} réponses sur le transport en ambulance à {CFG['CITY']}, la réservation, les transferts hospitaliers, les devis, les documents et les trajets réguliers."
        if CFG["CITY"] else
        f"FAQ TAMUDA INJAD : {len(FAQ_FLAT)} réponses sur la réservation d’une ambulance, les transferts hospitaliers, les devis, les documents et les trajets réguliers."
    )
    page(
        "/faq/",
        f"FAQ ambulance à {CFG['CITY']} : questions fréquentes | {NAME}" if CFG["CITY"] else f"FAQ : transport en ambulance | {NAME}",
        faq_desc, main, cr, [fq]
    )


def build_about():
    cr = [("À propos", None)]
    def tog(q, inner): return f'<details><summary>{E(q)}</summary><div class="answer">{inner}</div></details>'
    tel = f'<a href="tel:{E(CFG["PHONE_INTL"])}">{E(CFG["PHONE_DISPLAY"] or CFG["PHONE_INTL"])}</a>' if CFG["PHONE_INTL"] else todo("téléphone")
    em = f'<a href="mailto:{E(CFG["EMAIL"])}">{E(CFG["EMAIL"])}</a>' if CFG["EMAIL"] else todo("e-mail")
    zones = E(", ".join(CFG["AREAS"])) if CFG["AREAS"] else todo("zones desservies")
    ident = [("Dénomination", E(NAME)), ("Activité", "Transport en ambulance"),
             ("Ville", f'{val("CITY","ville")}, {val("COUNTRY","pays")}'),
             ("Adresse", f'{val("ADDRESS","adresse")}, {val("POSTAL","code postal")}'),
             ("Téléphone", tel), ("E-mail", em), ("Horaires", val("HOURS", "horaires confirmés")),
             ("Zones desservies", zones),
             ("Forme juridique et immatriculation", todo("à renseigner (voir Mentions légales)")),
             ("Agréments et autorisations", todo("références officielles vérifiées"))]
    ident_rows = "".join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a, b in ident)
    values = [("Clarté", "Chaque étape de la demande est expliquée : lieu, horaire, interlocuteur, modalités."),
              ("Prudence", "Le site donne des informations pratiques. Il ne pose aucun diagnostic et ne donne aucun conseil médical."),
              ("Coordination", "L’équipe échange avec les familles et les établissements pour organiser chaque trajet."),
              ("Confirmation", "Rien n’est considéré comme acquis : zone, horaire et équipements sont confirmés avant le transport.")]
    values_html = "".join(f'<div class="card"><span class="num" aria-hidden="true">✓</span><h3>{E(t)}</h3><p>{E(d)}</p></div>' for t, d in values)
    svc_cards = "".join(f'<a class="card link-card" href="/services/{s["slug"]}/"><span class="num">{i:02d}</span><h3>{E(s["name"])}</h3><p>{E(s["short"])}</p><span class="more">Voir la prestation →</span></a>' for i, s in enumerate(SERVICES, 1))
    steps = [("Votre demande", "Par téléphone ou via le formulaire de devis."), ("Étude", "Vérification de la faisabilité, de la zone et des disponibilités."), ("Confirmation", "Horaire, interlocuteur et modalités vous sont précisés."), ("Trajet", "Prise en charge au lieu convenu et remise à destination.")]
    st = '<ol class="steps">' + "".join(f"<li><h3>{a}</h3><p>{b}</p></li>" for a, b in steps) + "</ol>"
    soon = (tog("Notre histoire", f'<p>{todo("origine et dates, uniquement si confirmées")}</p>')
          + tog("L’équipe", f'<p>{todo("présentation de l’équipe réelle")}</p>')
          + tog("La flotte", f'<p>{todo("véhicules réels, sans chiffre non vérifié")}</p>')
          + tog("Agréments et autorisations", f'<p>{todo("documents officiels vérifiés")}</p>'))
    faq_items = [FAQ_FLAT[i] for i in (19, 20, 21, 11)]
    main = phero(f"À propos de {NAME}", f"{NAME} est une entreprise de transport en ambulance : elle organise des trajets en lien avec les familles et les établissements, avec des informations claires à chaque étape.", cr) + f'''
<section class="section" aria-labelledby="h-qui"><div class="container two-col"><div><span class="eyebrow">Qui sommes-nous ?</span><h2 id="h-qui">Une entreprise de transport en ambulance à {E(CFG["CITY"])}</h2>
<p>{NAME} organise des transports en ambulance à {E(CFG["CITY"])} et dans sa région, en lien avec les familles et les établissements. Nous nous attachons à expliquer clairement chaque étape de la demande.</p>
<p>Le site présente sept prestations, une zone d’intervention et une demande de devis personnalisé. Les informations qui dépendent de l’entreprise sont confirmées directement avec elle.</p>
<div class="btn-row"><a class="btn btn-primary" href="/contact/">Nous contacter</a><a class="btn btn-secondary" href="/services/">Voir les services</a></div></div>
<div><div class="table-wrap" role="region" aria-labelledby="cap-ident" tabindex="0" style="margin-top:0"><table style="min-width:0"><caption id="cap-ident">Fiche d’identité de {NAME}</caption>
<thead><tr><th scope="col">Information</th><th scope="col">Détail</th></tr></thead><tbody>{ident_rows}</tbody></table></div></div></div></section>
<section class="section soft" aria-labelledby="h-valeurs"><div class="container"><span class="eyebrow">Notre approche</span><h2 id="h-valeurs">Comment nous travaillons</h2>
<div class="grid cols-2" style="margin-top:1.5rem">{values_html}</div></div></section>
<section class="section" aria-labelledby="h-prestations"><div class="container"><span class="eyebrow">Nos prestations</span><h2 id="h-prestations">Ce que nous organisons</h2>
<div class="grid cols-3" style="margin-top:1.5rem">{svc_cards}</div></div></section>
<section class="section soft" aria-labelledby="h-deroule"><div class="container two-col"><div><span class="eyebrow">Déroulement</span><h2 id="h-deroule">De la demande au trajet</h2>{st}</div>
<div><span class="eyebrow">Transparence</span><h2>Informations à venir</h2><p>Ces rubriques seront complétées uniquement avec des informations réelles et vérifiées.</p>{soon}</div></div></section>
<section class="section" aria-labelledby="h-zone-ap"><div class="container"><span class="eyebrow">Zone d’intervention</span><h2 id="h-zone-ap">Où intervenons-nous ?</h2>{chips_html()}<p><a href="/zone-intervention/">Voir la page Zone &amp; carte</a></p></div></section>
<section class="section soft" aria-labelledby="h-faq-ap"><div class="container prose"><span class="eyebrow">FAQ</span><h2 id="h-faq-ap">Questions sur l’entreprise et le site</h2>{faq_details(faq_items)}<p><a href="/faq/">Toutes les questions</a></p></div></section>
{final_cta()}'''
    ld = [{"@context": "https://schema.org", "@type": "AboutPage", "name": f"À propos de {NAME}", "url": absu("/a-propos/"), "inLanguage": "fr", "about": {"@type": "Organization", "name": NAME, "url": absu("/")}},
          org_ld(),
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_items]}]
    page("/a-propos/", f"À propos de {NAME} : ambulance à {CFG['CITY']}",
         f"Découvrez {NAME}, entreprise de transport en ambulance à {CFG['CITY']} : approche, prestations, zone d’intervention et coordonnées.",
         main, cr, ld)

# ───────────── TÉMOIGNAGES : DONNÉES + CARROUSEL ─────────────
# ➜ Ajoutez vos témoignages RÉELS (reçus via Formspree, validés par leur auteur) ici,
#   OU dans un fichier temoignages.json placé à côté de build.py (même format, liste d'objets).
#   Puis relancez :  python3 build.py
#   Champs : prenom, ville, contexte (logistique uniquement), note (1 à 5), texte, date ("AAAA-MM")
TESTIMONIALS = [
    dict(prenom="Samira B.", ville="Tétouan", contexte="Trajet régulier",
         note=5, texte="Ponctualité et écoute à chaque trajet.", date="2026-10"),
    dict(prenom="Youssef A.", ville="Martil", contexte="Retour à domicile",
         note=5, texte="Équipe rassurante, prise en charge rapide.", date="2026-09"),
    dict(prenom="Fatima Z.", ville="Tanger", contexte="Transfert hospitalier",
         note=4, texte="Bonne communication avec ma famille.", date="2026-08"),
]

_tj = os.path.join(ROOT, "temoignages.json")
if os.path.exists(_tj):
    TESTIMONIALS += json.load(open(_tj, encoding="utf-8"))
MOIS = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
def t_clean():
    out = []
    for t in TESTIMONIALS:
        if not (t.get("texte") and t.get("prenom")): continue
        n = max(1, min(5, int(t.get("note", 5))))
        out.append({**t, "note": n})
    return sorted(out, key=lambda t: t.get("date", ""), reverse=True)
def t_date(d):
    try: y, m = d.split("-")[:2]; return f"{MOIS[int(m)-1]} {y}"
    except Exception: return ""
def t_assets(): return dict(extra_css=["/assets/css/testimonials.css"], extra_js=["/assets/js/testimonials.js"]) if t_clean() else {}

def testi_carousel(home=False):
    """Carrousel accessible (scroll-snap natif + JS d'amélioration). Vide → rien (accueil) ou message (page témoignages)."""
    ts = t_clean()
    if not ts:
        if home: return ""
        return ('<section class="section" aria-labelledby="h-avis"><div class="container"><span class="eyebrow">Avis publiés</span>'
                '<h2 id="h-avis">Témoignages</h2><div class="empty"><p>Les retours authentiques apparaîtront ici, sous forme de carrousel, '
                'dès qu’ils auront été recueillis et validés avec leur auteur.</p></div></div></section>')
    n = len(ts)
    slides = "".join(
        f'<article class="t-slide" role="group" aria-roledescription="diapositive" aria-label="{i} sur {n}"><div class="card review-card">'
        f'<span class="t-quote" aria-hidden="true">“</span>'
        f'<span class="review-stars" role="img" aria-label="Note : {t["note"]} sur 5">{"★"*t["note"]}<span class="off">{"★"*(5-t["note"])}</span></span>'
        f'<blockquote class="review-body"><p>{E(t["texte"])}</p></blockquote>'
        f'<footer class="review-header"><span class="review-avatar" aria-hidden="true">{E(t["prenom"].strip()[:1].upper())}</span>'
        f'<div><strong class="review-author">{E(t["prenom"])}</strong>'
        f'<span class="review-meta">{E(t.get("ville",""))}{" · " + E(t["contexte"]) if t.get("contexte") else ""}</span></div></footer>'
        f'<p class="meta t-pub">Publié avec l’accord de l’auteur{" · " + t_date(t.get("date","")) if t.get("date") else ""}</p></div></article>'
        for i, t in enumerate(ts, 1))
    avg = sum(t["note"] for t in ts) / n
    head = ('<span class="eyebrow">Avis publiés</span><h2 id="h-avis">Ce que disent les personnes transportées</h2>'
            f'<p class="lead">{n} témoignage{"s" if n > 1 else ""} publié{"s" if n > 1 else ""} avec l’accord de leurs auteurs · note moyenne {avg:.1f}/5.</p>')
    more = '' if not home else '<p style="margin-top:1rem"><a href="/temoignages/">Voir tous les témoignages et laisser le vôtre</a></p>'
    return (f'<section class="section{" soft" if home else ""}" aria-labelledby="h-avis"><div class="container">{head}'
            f'<div class="t-carousel" data-carousel role="region" aria-roledescription="carrousel" aria-label="Témoignages">'
            f'<div class="t-track" tabindex="0">{slides}</div>'
            f'<div class="t-controls"><button class="t-btn t-prev" type="button" aria-label="Témoignage précédent">‹</button>'
            f'<div class="t-dots" aria-label="Choisir un groupe de témoignages"></div>'
            f'<button class="t-btn t-pause" type="button" aria-pressed="false" aria-label="Mettre en pause le défilement automatique">❚❚</button>'
            f'<button class="t-btn t-next" type="button" aria-label="Témoignage suivant">›</button></div>'
            f'<p class="sr-only t-count" role="status" aria-live="polite"></p></div>{more}</div></section>')

TESTI_CSS = r"""/* Carrousel de témoignages — généré par build.py */
.t-carousel{position:relative;margin-top:1.5rem}
.t-track{--per:1;display:flex;gap:1.25rem;overflow-x:auto;scroll-snap-type:x mandatory;scroll-behavior:smooth;
  padding:.5rem .25rem 1rem;scrollbar-width:thin;-webkit-overflow-scrolling:touch;outline-offset:4px}
@media(min-width:760px){.t-track{--per:2}}
@media(min-width:1100px){.t-track{--per:3}}
.t-slide{flex:0 0 calc((100% - (var(--per) - 1) * 1.25rem) / var(--per));scroll-snap-align:start;display:flex}
.t-slide .review-card{position:relative;display:flex;flex-direction:column;gap:.75rem;width:100%;padding:1.5rem 1.4rem 1.2rem;
  border-top:4px solid var(--red,#c8102e);height:100%}
.t-quote{position:absolute;top:.1rem;right:1rem;font:700 4.5rem/1 Georgia,serif;color:var(--navy,#203566);opacity:.1;pointer-events:none}
.review-stars{color:#e8a317;letter-spacing:.12em;font-size:1.15rem}.review-stars .off{color:#cfd5e3}
.review-body{margin:0;flex:1}.review-body p{margin:0;font-size:1.02rem;line-height:1.6}
.review-header{display:flex;align-items:center;gap:.75rem}
.review-avatar{display:grid;place-items:center;width:2.6rem;height:2.6rem;border-radius:50%;background:var(--navy,#203566);color:#fff;font-weight:700}
.review-author{display:block}.review-meta{display:block;font-size:.88rem;opacity:.75}.t-pub{margin:0;font-size:.82rem}
.t-controls{display:none;align-items:center;justify-content:center;gap:.6rem;margin-top:.5rem}
.js .t-controls{display:flex}.t-carousel.is-static .t-controls{display:none}
.t-btn{width:2.75rem;height:2.75rem;border-radius:50%;border:2px solid var(--navy,#203566);background:#fff;color:var(--navy,#203566);
  font-size:1.4rem;line-height:1;cursor:pointer;transition:background .2s,color .2s}
.t-btn:hover,.t-btn:focus-visible{background:var(--navy,#203566);color:#fff}.t-pause{font-size:.75rem}
.t-dots{display:flex;gap:.45rem}
.t-dot{width:.8rem;height:.8rem;border-radius:50%;border:0;background:#c5cde0;cursor:pointer;padding:0;position:relative}
.t-dot::after{content:"";position:absolute;inset:-.6rem}
.t-dot[aria-current="true"]{background:var(--red,#c8102e);transform:scale(1.25)}
@media(prefers-reduced-motion:reduce){.t-track{scroll-behavior:auto}}
/* Étoiles du formulaire (radios, de gauche à droite : 1 → 5) */
.star-fieldset{border:0;padding:0;margin:0}.star-fieldset legend{font-weight:600;margin-bottom:.4rem}
.star-group{display:inline-flex;flex-direction:row-reverse;gap:.15rem}
.star-group input{position:absolute;opacity:0;width:1px;height:1px}
.star-group label{font-size:2rem;line-height:1;color:#cfd5e3;cursor:pointer;transition:color .15s}
.star-group label:hover,.star-group label:hover~label,.star-group input:checked~label{color:#e8a317}
.star-group input:focus-visible+label{outline:3px solid var(--navy,#203566);outline-offset:2px;border-radius:4px}
"""

TESTI_JS = r"""/* Carrousel de témoignages — généré par build.py */
(function(){
  function init(root){
    var track=root.querySelector(".t-track"),slides=[].slice.call(track.children),
        dotsBox=root.querySelector(".t-dots"),prev=root.querySelector(".t-prev"),next=root.querySelector(".t-next"),
        pause=root.querySelector(".t-pause"),count=root.querySelector(".t-count"),
        reduce=window.matchMedia("(prefers-reduced-motion: reduce)").matches,
        playing=!reduce,hover=false,timer=null,page=0;
    function per(){return Math.max(1,Math.round(track.clientWidth/slides[0].offsetWidth));}
    function pages(){return Math.ceil(slides.length/per());}
    function step(){return slides.length>1?slides[1].offsetLeft-slides[0].offsetLeft:track.clientWidth;}
    function drawDots(){
      dotsBox.innerHTML="";
      for(var i=0;i<pages();i++){(function(i){
        var b=document.createElement("button");b.type="button";b.className="t-dot";
        b.setAttribute("aria-label","Groupe "+(i+1)+" sur "+pages());
        b.addEventListener("click",function(){go(i,true);});dotsBox.appendChild(b);})(i);}
      root.classList.toggle("is-static",pages()<2);mark();
    }
    function mark(){
      [].forEach.call(dotsBox.children,function(d,i){i===page?d.setAttribute("aria-current","true"):d.removeAttribute("aria-current");});
      var a=page*per()+1,z=Math.min(slides.length,a+per()-1);
      count.textContent="Témoignages "+a+(z>a?" à "+z:"")+" sur "+slides.length;
    }
    function go(p,user){
      var n=pages();page=(p+n)%n;
      track.scrollTo({left:page*per()*step(),behavior:reduce?"auto":"smooth"});mark();
      if(user)restart();
    }
    var tick;track.addEventListener("scroll",function(){
      clearTimeout(tick);tick=setTimeout(function(){
        var p=Math.round(track.scrollLeft/(per()*step()));
        if(track.scrollLeft+track.clientWidth>=track.scrollWidth-2)p=pages()-1;
        if(p!==page){page=Math.max(0,Math.min(pages()-1,p));mark();}},90);},{passive:true});
    function stop(){clearInterval(timer);timer=null;}
    function restart(){stop();if(playing&&!hover&&!document.hidden&&pages()>1)timer=setInterval(function(){go(page+1);},6500);}
    prev.addEventListener("click",function(){go(page-1,true);});
    next.addEventListener("click",function(){go(page+1,true);});
    pause.addEventListener("click",function(){
      playing=!playing;pause.setAttribute("aria-pressed",String(!playing));
      pause.textContent=playing?"❚❚":"▶";
      pause.setAttribute("aria-label",playing?"Mettre en pause le défilement automatique":"Reprendre le défilement automatique");restart();});
    track.addEventListener("keydown",function(e){
      if(e.key==="ArrowRight"){e.preventDefault();go(page+1,true);}
      if(e.key==="ArrowLeft"){e.preventDefault();go(page-1,true);}});
    ["mouseenter","focusin","touchstart"].forEach(function(ev){root.addEventListener(ev,function(){hover=true;stop();},{passive:true});});
    ["mouseleave","focusout"].forEach(function(ev){root.addEventListener(ev,function(){hover=false;restart();});});
    document.addEventListener("visibilitychange",restart);
    window.addEventListener("resize",function(){drawDots();go(Math.min(page,pages()-1));});
    if(reduce){pause.setAttribute("aria-pressed","true");pause.textContent="▶";
      pause.setAttribute("aria-label","Activer le défilement automatique");}
    drawDots();restart();
  }
  function ready(){[].forEach.call(document.querySelectorAll("[data-carousel]"),init);}
  document.readyState==="loading"?document.addEventListener("DOMContentLoaded",ready):ready();
})();
"""
def write_testi_assets():
    for rel, txt in (("assets/css/testimonials.css", TESTI_CSS), ("assets/js/testimonials.js", TESTI_JS)):
        fp = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, "w", encoding="utf-8").write(txt)

def testi_form():
    ep = E(CFG["REVIEWS_ENDPOINT"] or CFG["FORM_ENDPOINT"])
    stars = "".join(f'<input type="radio" id="star{k}" name="note" value="{k} étoile{"s" if k>1 else ""}"{" required" if k==5 else ""}>'
                    f'<label for="star{k}" title="{k} étoile{"s" if k>1 else ""} – {t}">★</label>'
                    for k, t in ((5,"Excellent"),(4,"Très bien"),(3,"Bien"),(2,"Passable"),(1,"Insuffisant")))
    return f"""{NOJS}<form class="form" id="form-temoignage" data-form method="post" data-endpoint="{ep}">
<input type="hidden" name="_subject" value="Nouveau témoignage à valider – {NAME}">
<div style="position:absolute;left:-9999px" aria-hidden="true"><label>Ne pas remplir<input name="website" tabindex="-1" autocomplete="off"></label></div>
<div class="form-grid two">
{fld("r-prenom","Prénom ou initiales",ac="given-name").replace('name="r-prenom"','name="prenom"')}
{fld("r-ville","Ville du transport").replace('name="r-ville"','name="ville"')}
{fld("r-contexte","Contexte du trajet",hint="Ex. : transfert hospitalier, trajet régulier, retour à domicile… (sans détail médical)").replace('name="r-contexte"','name="contexte"')}
{fld("r-email","E-mail",typ="email",req=False,hint="Uniquement si vous souhaitez être informé(e) de la publication.",ac="email").replace('name="r-email"','name="email"')}
<div class="field full"><fieldset class="star-fieldset"><legend>Note globale <span class="req" aria-hidden="true">*</span></legend><div class="star-group" role="group">{stars}</div></fieldset></div>
<div class="field full"><label for="r-message">Votre témoignage <span class="req" aria-hidden="true">*</span></label><span class="hint" id="r-message-h">Décrivez l’organisation du transport (prise en charge, communication, ponctualité…). Aucune information médicale, s’il vous plaît.</span><textarea id="r-message" name="message" required rows="5" maxlength="700" aria-describedby="r-message-h"></textarea></div>
<div class="field full"><div class="check"><input type="checkbox" id="r-consent-pub" name="consent_publication" value="oui" required><label for="r-consent-pub">J’accepte que ce témoignage soit publié sur le site de {NAME}, avec mon prénom (ou initiales) et la ville du transport. <span class="req" aria-hidden="true">*</span></label></div></div>
<div class="field full"><div class="check"><input type="checkbox" id="r-consent-rgpd" name="consent_rgpd" value="oui" required><label for="r-consent-rgpd">J’ai pris connaissance de la <a href="/politique-confidentialite/">politique de confidentialité</a> et j’accepte que ces informations soient utilisées pour traiter et publier mon témoignage. <span class="req" aria-hidden="true">*</span></label></div></div>
</div><p class="meta">Ne saisissez ni diagnostic, ni information de santé, ni numéro d’assuré.<br>Droit de retrait à tout moment : <a href="/contact/">page Contact</a>.</p>
<div class="btn-row"><button class="btn btn-primary" type="submit">Envoyer mon témoignage</button></div>{form_status()}</form>"""

def build_testi():
    cr = [("Témoignages", None)]
    ts = t_clean(); n = len(ts)
    stats = [(str(n) if n else "0", "témoignage publié avec l’accord de son auteur" if n < 2 else "témoignages publiés avec l’accord de leurs auteurs")]
    stats += [("100 %", "des témoignages publiés avec le consentement de leur auteur"), ("0", "avis acheté, échangé ou simulé")]
    stats_html = '<div class="stats">' + "".join(f'<div class="stat"><strong>{a}</strong><span>{E(b)}</span></div>' for a, b in stats) + '</div>'
    eng = [("Transparence", "Chaque témoignage publié indique qui l’a écrit et dans quel contexte : aucun retour n’est présenté sans ces précisions."),
           ("Consentement", "Un témoignage n’est publié qu’après accord explicite de son auteur, qui peut demander son retrait à tout moment."),
           ("Authenticité", "Seuls des retours réels sont publiés. Aucun avis n’est acheté, échangé ni rédigé par l’entreprise."),
           ("Vie privée", "Aucun détail médical n’est reproduit dans un témoignage : seules les circonstances logistiques du transport sont décrites.")]
    eng_html = "".join(f'<div class="card"><span class="num" aria-hidden="true">✓</span><h3>{E(t)}</h3><p>{E(d)}</p></div>' for t, d in eng)
    steps = [("Le transport est réalisé", "À l’issue du trajet, l’équipe peut proposer à la personne ou à son proche de laisser un retour."),
             ("L’auteur rédige son retour", "Dans ses propres mots, sur les circonstances du transport : organisation, prise en charge, communication."),
             ("L’accord est recueilli", "L’auteur valide le texte et les informations qui apparaîtront (prénom, ville, contexte). Il peut refuser ou corriger à tout moment."),
             ("Le témoignage est publié", "Il apparaît dans le carrousel de cette page avec son contexte ; il peut être retiré sur simple demande de l’auteur.")]
    st = '<ol class="steps">' + "".join(f"<li><h3>{a}</h3><p>{b}</p></li>" for a, b in steps) + "</ol>"
    privacy_rows = (
        '<tr><th scope="row">Prénom ou initiales de l’auteur</th><td>Avec son accord, oui</td><td>Nom complet, sans accord écrit</td></tr>'
        '<tr><th scope="row">Ville du transport</th><td>Avec son accord, oui</td><td>Adresse exacte, établissement nommé sans accord</td></tr>'
        '<tr><th scope="row">Circonstances logistiques (type de trajet, organisation)</th><td>Oui, si l’auteur les mentionne</td><td>Diagnostic, état de santé, traitements</td></tr>'
        '<tr><th scope="row">Coordonnées de l’auteur (téléphone, e-mail)</th><td>Jamais</td><td>Jamais, quelle que soit la situation</td></tr>')
    faqs = [("Pourquoi valider mon accord avant publication ?", "Votre témoignage est un contenu personnel : il n’est publié qu’avec votre consentement explicite, matérialisé par la case à cocher du formulaire. Vous pouvez demander son retrait à tout moment via la page Contact."),
            ("Comment laisser un retour sur un transport ?", "Utilisez le formulaire de cette page ou contactez l’entreprise par téléphone ou via la page Contact en précisant la date du transport."),
            ("Puis-je demander le retrait de mon témoignage ?", "Oui, à tout moment et sans justification : contactez l’entreprise et le texte est retiré du carrousel."),
            ("Faut-il laisser un avis ailleurs (plateformes) ?", "C’est votre choix. Si l’entreprise référence une plateforme d’avis, le lien figure sur cette page ; les conditions d’utilisation de ces plateformes s’appliquent à ces publications.")]
    link = f'<p><a class="btn btn-secondary" href="{E(CFG["REVIEWS_LINK"])}" rel="noopener" target="_blank">Lire les avis (nouvel onglet)</a></p>' if CFG["REVIEWS_LINK"] else ""
    links = ('<a class="card link-card" href="/services/"><h3>Nos services</h3><p>Les sept prestations de transport en ambulance et leurs modalités à confirmer.</p><span class="more">Voir les services →</span></a>'
             '<a class="card link-card" href="/tarifs-devis/"><h3>Tarifs &amp; devis</h3><p>Préparez votre demande de devis avec les informations logistiques utiles.</p><span class="more">Demander un devis →</span></a>'
             '<a class="card link-card" href="/contact/"><h3>Contact</h3><p>Téléphone, e-mail et formulaire pour joindre l’équipe.</p><span class="more">Nous contacter →</span></a>')
    main = phero("Témoignages : retours des personnes transportées",
                 f"Les retours authentiques des personnes transportées par {NAME} et de leurs proches, publiés uniquement avec leur accord explicite.", cr) + f'''
<section class="section stats-wrap" aria-label="Chiffres clés"><div class="container">{stats_html}</div></section>
{testi_carousel()}
<section class="section soft" aria-labelledby="h-deposer"><div class="container two-col wide-left"><div><span class="eyebrow">Laisser un avis</span><h2 id="h-deposer">Partagez votre expérience</h2>
<p>Votre retour aide d’autres personnes à se préparer. Il est relu, puis publié dans le carrousel uniquement avec votre accord explicite ; il peut être retiré à tout moment.</p>{testi_form()}{link}</div>
<aside><div class="card"><span class="num" aria-hidden="true">✓</span><h2 style="font-size:1.1rem">Ce qui sera publié</h2><ul class="ticks"><li>Votre prénom ou initiales</li><li>La ville du transport</li><li>Le contexte du trajet (logistique uniquement)</li><li>Votre note et le texte de votre témoignage</li></ul></div>
<div class="card" style="margin-top:1rem"><span class="num" aria-hidden="true">✗</span><h2 style="font-size:1.1rem">Ce qui ne sera jamais publié</h2><ul class="ticks"><li>Votre nom complet (sauf demande)</li><li>Votre adresse exacte</li><li>Toute information médicale</li><li>Votre e-mail ou téléphone</li></ul></div>
<div class="notice" style="margin-top:1rem"><p>Votre témoignage est relu avant publication.<br>Droit de retrait à tout moment : <a href="/contact/">page Contact</a>.</p></div></aside></div></section>
<section class="section" aria-labelledby="h-cadence"><div class="container"><span class="eyebrow">Nos engagements</span><h2 id="h-cadence">Comment les témoignages sont gérés</h2>
<p class="lead">Cette page n’affiche que des retours réels : voici les règles qui encadrent chaque publication.</p><div class="grid cols-2" style="margin-top:1.5rem">{eng_html}</div></div></section>
<section class="section soft" aria-labelledby="h-recueil"><div class="container"><span class="eyebrow">Déroulement</span><h2 id="h-recueil">Du transport au témoignage : les quatre étapes</h2>
<p class="lead">Aucun retour n’est publié sans avoir suivi ce processus, du recueil du texte au droit de retrait.</p>{st}</div></section>
<section class="section" aria-labelledby="h-privacite"><div class="container"><span class="eyebrow">Vie privée</span><h2 id="h-privacite">Ce qui apparaît — et n’apparaît jamais — dans un témoignage</h2>
<div class="table-wrap" role="region" aria-labelledby="cap-privacite" tabindex="0"><table><caption id="cap-privacite">Informations publiées ou exclues dans les témoignages de {NAME}</caption>
<thead><tr><th scope="col">Information</th><th scope="col">Publication</th><th scope="col">Jamais publié / conditions</th></tr></thead><tbody>{privacy_rows}</tbody></table></div>
<div class="notice info" style="margin-top:1.25rem"><p><strong>Pas de détail médical.</strong> Un témoignage décrit l’organisation du transport, jamais la santé de la personne transportée.</p></div></div></section>
<section class="section soft" aria-labelledby="h-faq-t"><div class="container prose"><span class="eyebrow">FAQ</span><h2 id="h-faq-t">Questions fréquentes sur les témoignages</h2>{faq_details(faqs)}<p><a href="/faq/">Voir la FAQ complète du site</a></p></div></section>
<section class="section" aria-labelledby="h-liens-t"><div class="container"><span class="eyebrow">Pour aller plus loin</span><h2 id="h-liens-t">Découvrir {NAME}</h2><div class="grid cols-3" style="margin-top:1.5rem">{links}</div></div></section>
{final_cta("Votre avis compte : parlons de votre trajet")}'''
    ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Témoignages", "url": absu("/temoignages/"), "inLanguage": "fr",
           "about": {"@type": "Organization", "name": NAME, "url": absu("/")}}, org_ld(),
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs[:3]]}]
    page("/temoignages/", f"Témoignages clients – transport en ambulance | {NAME}",
         f"Partagez votre expérience avec {NAME} à {CFG['CITY']} : témoignages authentiques en carrousel, consentement explicite, vie privée protégée, droit de retrait. Aucun avis inventé.",
         main, cr, ld, **t_assets())

# Blog
ARTICLES = [
dict(slug="preparer-un-transport-en-ambulance", title="Préparer un transport en ambulance : la checklist pratique",
 desc="Les informations pratiques à rassembler avant un transport en ambulance, pour que la prise en charge se passe simplement.",
 sections=[("Pourquoi préparer ?","Un transport se déroule mieux quand les informations de base sont connues à l’avance : où, quand, vers quel service. Cette liste porte uniquement sur la logistique."),
  ("Avant l’appel",["Notez l’adresse exacte, l’étage et les accès (ascenseur, marches).","Repérez le nom de l’établissement de destination et du service.","Rassemblez le nom et le numéro d’une personne joignable."]),
  ("Le jour du transport",["Prévoyez que quelqu’un attende au point de prise en charge.","Gardez les documents demandés à portée de main.","Prévenez l’équipe en cas de changement d’horaire."]),
  ("Et ensuite ?","Pour obtenir un tarif, consultez la page <a href=\"/tarifs-devis/\">Tarifs &amp; devis</a>. Pour choisir une prestation, voyez nos <a href=\"/services/\">services</a>.")]),
dict(slug="organiser-des-trajets-reguliers", title="Organiser des trajets réguliers : planning et interlocuteur",
 desc="Comment structurer des transports récurrents : calendrier, point de prise en charge, gestion des changements.",
 sections=[("Pourquoi un cadre ?","Lorsqu’un trajet se répète, quelques règles simples évitent les oublis : un calendrier partagé, un contact unique et une manière claire de signaler les changements."),
  ("Construire le planning",["Listez les dates et horaires de début de chaque rendez-vous.","Précisez le lieu et le point de prise en charge.","Indiquez si un retour est à prévoir."]),
  ("Gérer les imprévus",["Prévenez l’entreprise dès qu’un horaire change.","Gardez un numéro direct à disposition.","Vérifiez avec l’équipe le délai de prévenance attendu."]),
  ("Aller plus loin","Découvrez la prestation <a href=\"/services/dialyse-chimiotherapie/\">Dialyse &amp; chimiothérapie</a>, qui illustre l’organisation de trajets récurrents, et la <a href=\"/faq/\">FAQ</a>.")]),
dict(slug="informations-pour-un-devis-de-transport", title="Informations à préparer pour obtenir un devis de transport",
 desc="Les informations logistiques utiles pour demander un devis de transport en ambulance, sans données médicales.",
 sections=[("Un devis plus rapide","Plus la demande est précise, plus la réponse est rapide. Voici les informations qui font généralement la différence."),
  ("Le trajet",["Adresse ou ville de départ, destination.","Date, heure et éventuelle flexibilité.","Aller simple, aller-retour ou trajets répétés."]),
  ("Le contexte pratique",["Mobilité : allongé, assis, fauteuil roulant.","Accès au lieu : étage, ascenseur, escaliers.","Présence d’un accompagnant."]),
  ("Ce qu’il ne faut pas envoyer","Ne transmettez pas de diagnostic ou de dossier médical dans un formulaire en ligne. Rendez-vous sur <a href=\"/tarifs-devis/\">Tarifs &amp; devis</a> pour faire votre demande.")]),
]
def article_body(a):
    out = ""
    for h, c in a["sections"]:
        out += f"<h2>{h}</h2>" + (ul(c) if isinstance(c, list) else f"<p>{c}</p>")
    return out
def article_main(a, cr):
    return crumb_html(cr).join(['<section class="page-hero"><div class="container">', f'<h1>{E(a["title"])}</h1><p class="meta">Publié le {a["date"]} · Par l’équipe {NAME} · Information pratique, sans valeur de conseil médical</p></div><div class="ridge sm" aria-hidden="true"></div></section>']) + f'''
<section class="section"><div class="container prose"><p class="lead">{E(a["desc"])}</p>{article_body(a)}
<div class="notice info"><p>Cet article ne contient ni diagnostic ni conseil thérapeutique. Pour toute question de santé, adressez-vous à un professionnel de santé.</p></div>{ctas()}
<p><a href="/blog/">← Retour au blog</a></p></div></section>'''
def build_blog():
    cr = [("Blog", None)]
    cards = "".join(f'<a class="card link-card" href="/blog/{a["slug"]}/"><h2 style="font-size:1.25rem">{E(a["title"])}</h2><p>{E(a["desc"])}</p><span class="more">Lire l’article →</span></a>' for a in ARTICLES)
    main = phero("Blog : conseils pratiques", "Des articles pour préparer vos transports. Informations logistiques uniquement, sans conseil médical.", cr) + f'<section class="section"><div class="container"><div class="grid cols-3">{cards}</div></div></section>'
    page("/blog/", f"Blog : préparer un transport en ambulance | {NAME}", "Articles pratiques sur la préparation d’un transport, les trajets réguliers et les informations utiles pour un devis.", main, cr)
    for a in ARTICLES:
        a["date"] = TODAY
        path = f"/blog/{a['slug']}/"
        cr2 = [("Blog", "/blog/"), (a["title"], None)]
        bp = {"@context":"https://schema.org","@type":"BlogPosting","headline":a["title"],"description":a["desc"],
              "datePublished":TODAY,"dateModified":TODAY,"inLanguage":"fr",
              "author":{"@type":"Organization","name":NAME},
              "publisher":{"@type":"Organization","name":NAME,"logo":{"@type":"ImageObject","url":absu(LOGO)}},
              "mainEntityOfPage":{"@type":"WebPage","@id":absu(path)}}
        if CONF: bp["image"] = absu(LOGO)
        page(path, f"{a['title']} | {NAME}", a["desc"], article_main(a, cr2), cr2, [bp], og="article")
    # Modèle réutilisable (non indexé, hors sitemap)
    tpl = dict(title="[Titre de l’article]", desc="[Résumé de l’article en une ou deux phrases]", date="[AAAA-MM-JJ]",
        sections=[("[Titre de section]","[Paragraphe d’introduction]"),("[Liste]",["[Point 1]","[Point 2]"]),("Pour aller plus loin","[Liens internes vers <a href=\"/services/\">Services</a> ou <a href=\"/tarifs-devis/\">Tarifs &amp; devis</a>]")])
    cr3 = [("Blog", "/blog/"), ("[Titre de l’article]", None)]
    page("/modeles/article-modele/", "Modèle d’article | " + NAME, "Modèle réutilisable d’article de blog.", article_main(tpl, cr3), cr3, index=False, file="modeles/article-modele.html")

def legal_row(t, l): return f"<h2>{t}</h2><p>{todo(l)}</p>"
def build_legal():
    cr = [("Mentions légales", None)]
    notice = '<div class="notice warn"><p><strong>Modèle à compléter.</strong> Ce texte est une trame : il doit être adapté au pays, à l’entité juridique et aux outils réellement utilisés, idéalement avec un professionnel du droit. Il ne garantit pas, en l’état, la conformité juridique.</p></div>'
    body = notice + f'''<h2>Éditeur du site</h2><ul class="ticks"><li>Dénomination : {NAME}</li><li>Forme juridique : {todo("forme juridique")}</li><li>Numéro d’immatriculation : {todo("numéro d’enregistrement")}</li><li>Adresse : {val("ADDRESS","adresse")}, {val("POSTAL","code postal")} {val("CITY","ville")}, {val("COUNTRY","pays")}</li><li>Téléphone : {val("PHONE_DISPLAY","téléphone")}</li><li>E-mail : {val("EMAIL","e-mail")}</li><li>Responsable de publication : {todo("nom")}</li></ul>
{legal_row("Agréments et autorisations","références des autorisations de transport sanitaire vérifiées")}
{legal_row("Hébergeur","nom, adresse et contact de l’hébergeur")}
{legal_row("Propriété intellectuelle","règles applicables aux contenus et au logo")}
{legal_row("Responsabilité","limites de responsabilité selon le droit applicable")}
{legal_row("Droit applicable et juridiction","selon le pays et l’entité")}'''
    main = phero("Mentions légales", "Informations sur l’éditeur et l’hébergeur du site.", cr) + f'<section class="section"><div class="container prose">{body}</div></section>'
    page("/mentions-legales/", f"Mentions légales | {NAME}", "Mentions légales du site de TAMUDA INJAD : éditeur, hébergeur et informations juridiques.", main, cr)
    cr = [("Politique de confidentialité", None)]
    fields = ul(["Nom et téléphone", "E-mail (facultatif)", "Adresses de départ et de destination, date souhaitée, type de transport", "Contenu des champs libres (message, précisions)"])
    body = notice + f'''<h2>Responsable du traitement</h2><p>{NAME}, {val("ADDRESS","adresse")}, {val("CITY","ville")}. Contact : {val("EMAIL","e-mail de contact")}.</p>
<h2>Données collectées via les formulaires</h2>{fields}<p>Aucune information médicale ne doit être saisie dans les champs libres.</p>
<h2>Finalités</h2><p>Répondre aux demandes de contact et de devis. {todo("compléter si d’autres finalités")}</p>
{legal_row("Base légale","selon le droit applicable dans le pays")}
{legal_row("Destinataires","personnes et prestataires ayant accès aux données (messagerie, service d’envoi des formulaires, etc.)")}
{legal_row("Durée de conservation","durées par catégorie de données")}
{legal_row("Droits des personnes","droits applicables, modalités et autorité de contrôle")}
<h2>Cookies et traceurs</h2><p>Dans sa version actuelle, ce site n’utilise ni cookie publicitaire, ni outil de mesure d’audience. Si un tel service (analytics, carte externe, vidéo) est ajouté, cette page et le mécanisme de consentement doivent être mis à jour. {todo("à vérifier avant publication")}</p>
<h2>Carte externe</h2><p>Lorsqu’elle est activée, la carte n’est chargée qu’après action de l’utilisateur et peut transmettre des données (adresse IP) au fournisseur de cartographie. {todo("fournisseur et politique associée")}</p>'''
    main = phero("Politique de confidentialité", "Comment les données saisies sur ce site sont traitées.", cr) + f'<section class="section"><div class="container prose">{body}</div></section>'
    page("/politique-confidentialite/", f"Politique de confidentialité | {NAME}", "Politique de confidentialité de TAMUDA INJAD : données collectées, finalités, conservation et droits.", main, cr)

def build_contact():
    cr = [("Contact", None)]
    def tog(q, inner): return f'<details><summary>{E(q)}</summary><div class="answer">{inner}</div></details>'
    tel = f'<a href="tel:{E(CFG["PHONE_INTL"])}">{E(CFG["PHONE_DISPLAY"] or CFG["PHONE_INTL"])}</a>' if CFG["PHONE_INTL"] else todo("téléphone")
    em = f'<a href="mailto:{E(CFG["EMAIL"])}">{E(CFG["EMAIL"])}</a>' if CFG["EMAIL"] else todo("e-mail")
    addr = f'{val("ADDRESS","adresse")}, {val("POSTAL","code postal")} {val("CITY","ville")}'
    cards = [("☎", "Téléphone", tel, "Pour organiser ou modifier un trajet."),
             ("✉", "E-mail", em, "Pour une question ou l’envoi d’informations pratiques."),
             ("⌂", "Adresse", addr, f'{E(CFG["COUNTRY"])}'),
             ("◷", "Horaires", val("HOURS", "horaires confirmés"), "À confirmer directement avec l’entreprise.")]
    cards_html = "".join(f'<div class="card"><span class="num" aria-hidden="true">{i}</span><h3>{t}</h3><p style="color:var(--ink);font-weight:600;margin-bottom:.4em">{v}</p><p class="meta" style="margin:0">{n}</p></div>' for i, t, v, n in cards)
    canal = [("Urgence vitale", "Les secours compétents de votre pays", "Ce site et l’entreprise ne sont pas un service d’urgence."),
             ("Demande de prix", '<a href="/tarifs-devis/">Tarifs &amp; devis</a>', "Départ, destination, date, type de transport."),
             ("Question sur une prestation", '<a href="/services/">Pages Services</a> ou formulaire ci-dessus', "La prestation concernée et le contexte pratique."),
             ("Trajets réguliers", '<a href="/tarifs-devis/">Tarifs &amp; devis</a> ou téléphone', "Calendrier des séances, adresse du centre."),
             ("Suivi ou modification d’une demande", "Téléphone ou formulaire", "Un objet clair et un numéro joignable.")]
    canal_rows = "".join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in canal)
    form = (contact_form().replace('Utilisez les coordonnées de la page <a href="/contact/">Contact</a> pour joindre l’entreprise.', 'Utilisez les coordonnées indiquées sur cette page pour joindre l’entreprise.')
            .replace('Utilisez la page <a href="/contact/">Contact</a> pour joindre l’entreprise.', 'Utilisez les coordonnées indiquées sur cette page.'))
    tips = (tog("Pour une demande de trajet", ul(["Lieu de départ et destination.", "Date et heure souhaitées.", "Nom et numéro d’une personne joignable."]))
          + tog("Pour l’accès au lieu de prise en charge", ul(["Étage, ascenseur, marches éventuelles.", "Code d’accès ou point de rendez-vous."]))
          + tog("Ce qu’il ne faut pas écrire", "<p>Aucun diagnostic, dossier médical ni numéro d’assuré dans le message. L’entreprise vous indiquera le canal adapté si un document est nécessaire.</p>"))
    maptxt = map_text().replace("voir la liste ci-dessus", "voir la zone d’intervention ci-dessous")
    faq_items = [FAQ_FLAT[i] for i in (0, 3, 4, 10, 19)]
    main = phero("Contact : transport en ambulance à " + E(CFG["CITY"]), "Joignez l’équipe pour une question ou un trajet à organiser. Pour un prix, utilisez la page Tarifs &amp; devis.", cr) + f'''
<section class="section" aria-labelledby="h-coord"><div class="container"><span class="eyebrow">Coordonnées</span><h2 id="h-coord">Comment nous joindre</h2>
<div class="grid cols-2" style="margin-top:1.5rem">{cards_html}</div>
<div class="btn-row">{call_btn()}{quote_btn()}</div></div></section>
<section class="section soft" aria-labelledby="h-ecrire"><div class="container two-col wide-left"><div><span class="eyebrow">Formulaire</span><h2 id="h-ecrire">Nous écrire</h2>{form}<p class="meta">Données utilisées pour répondre à votre message. <a href="/politique-confidentialite/">Politique de confidentialité</a>.</p></div>
<aside><div class="notice"><p><strong>Urgence vitale ?</strong> Contactez immédiatement les secours compétents de votre pays. Ce site n’est pas un service d’urgence.</p></div>
<h2 style="font-size:1.3rem">Informations utiles à indiquer</h2>{tips}</aside></div></section>
<section class="section" aria-labelledby="h-canal"><div class="container"><span class="eyebrow">Orientation</span><h2 id="h-canal">Quel canal pour quelle demande ?</h2>
<div class="table-wrap" role="region" aria-labelledby="cap-canal" tabindex="0"><table><caption id="cap-canal">Canal de contact conseillé selon votre besoin</caption>
<thead><tr><th scope="col">Besoin</th><th scope="col">Canal</th><th scope="col">À indiquer</th></tr></thead><tbody>{canal_rows}</tbody></table></div></div></section>
<section class="section soft" aria-labelledby="h-carte"><div class="container two-col"><div><span class="eyebrow">Localisation</span><h2 id="h-carte">Carte et accès</h2>{map_box()}<div style="margin-top:1rem">{maptxt}</div></div>
<div><span class="eyebrow">Zone d’intervention</span><h2>Villes desservies</h2>{chips_html()}<p>Les zones sont à confirmer pour chaque trajet : <a href="/zone-intervention/">voir la page Zone &amp; carte</a>.</p></div></div></section>
<section class="section" aria-labelledby="h-faq-ct"><div class="container prose"><span class="eyebrow">FAQ</span><h2 id="h-faq-ct">Avant de nous contacter</h2>{faq_details(faq_items)}<p><a href="/faq/">Toutes les questions</a></p></div></section>'''
    org = org_ld()
    if CFG["PHONE_INTL"]: org["contactPoint"] = {"@type": "ContactPoint", "telephone": CFG["PHONE_INTL"], "contactType": "customer service"}
    ld = [{"@context": "https://schema.org", "@type": "ContactPage", "name": f"Contact {NAME}", "url": absu("/contact/"), "inLanguage": "fr"}, org,
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_items]}]
    page("/contact/", f"Contact et devis ambulance à {CFG['CITY']} | {NAME}",
         f"Contactez {NAME} à {CFG['CITY']} : téléphone, e-mail, adresse, horaires et formulaire pour organiser un transport en ambulance.",
         main, cr, ld)

def build_404():
    main = '<section class="section"><div class="container prose"><h1>Page introuvable</h1><p class="lead">La page demandée n’existe pas ou a été déplacée.</p><ul class="ticks"><li><a href="/">Retour à l’accueil</a></li><li><a href="/services/">Voir les services</a></li><li><a href="/contact/">Nous contacter</a></li></ul></div></section>'
    page("/404.html", f"Page introuvable | {NAME}", "La page demandée est introuvable.", main, index=False, file="404.html")

def build_seo_files():
    """sitemap.xml priorisé (priority + changefreq + lastmod) et robots.txt."""
    urls = [("/", "1.0", "weekly", TODAY), ("/services/", "0.9", "weekly", TODAY)]
    urls += [(f"/services/{s['slug']}/", "0.8", "monthly", TODAY) for s in SERVICES]
    urls += [("/zone-intervention/", "0.7", "monthly", TODAY), ("/tarifs-devis/", "0.8", "monthly", TODAY),
             ("/faq/", "0.7", "monthly", TODAY), ("/a-propos/", "0.6", "monthly", TODAY),
             ("/temoignages/", "0.5", "monthly", TODAY), ("/blog/", "0.7", "weekly", TODAY)]
    urls += [(f"/blog/{a['slug']}/", "0.6", "monthly", a.get("date", TODAY)) for a in ARTICLES]
    urls += [("/contact/", "0.7", "monthly", TODAY), ("/mentions-legales/", "0.3", "yearly", TODAY),
             ("/politique-confidentialite/", "0.3", "yearly", TODAY)]
    dom = CFG["DOMAIN"] or "https://DOMAINE-A-COMPLETER"
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u, pr, cf, lm in urls:
        sm += f'  <url><loc>{dom}{u}</loc><lastmod>{lm}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority></url>\n'
    sm += '</urlset>\n'
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(sm)
    if CFG["INDEXABLE"]: rb = f"User-agent: *\nAllow: /\nDisallow: /modeles/\n\nSitemap: {dom}/sitemap.xml\n"
    else: rb = "# Site en préparation : indexation désactivée. Passer INDEXABLE à True dans build.py à la mise en ligne.\nUser-agent: *\nDisallow: /\n"
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(rb)
    return urls

if __name__ == "__main__":
    write_testi_assets()
    build_home(); build_services()
    for s in SERVICES: build_service(s)
    build_zone(); build_tarifs(); build_faq(); build_about(); build_testi(); build_blog(); build_legal(); build_contact(); build_404()
    n = build_seo_files()
    print("Pages générées :", len(n) + 2, "| FAQ :", len(FAQ_FLAT), "questions")
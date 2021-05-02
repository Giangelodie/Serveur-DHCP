Fonctions pour fichier de configuration:

- extr_fic(fic, ligne): fonction qui prend en paramètre "fic" qui correspond au contenu du fichier de configuration ainsi que "ligne" un int qui correspond à l'information que nous souhaitons extraire du fichier de configuration. La fonction va chercher dans la ligne du fichier de configuration l'information qui est utile au serveur et lui retourner.

- set_opt(n): prend en paramètre une liste contenant les informations propre à l'option demandé, appelle extr_fic afin de retourner la liste correspondante à l'option a directement mettre dans le message.

- set_bail(n): prend en paramètre une liste contenant les informations propre à l'option du bail, appelle extr_fic et modifie les caractères afin de les avoir dans le type souhaité et pouvoir mettre la liste telle quelle dans le message.

- plage_addr(text, line): fonction qui prend en paramètre "text" qui correspond au contenu du fichier de configuration ainsi que "line" un int qui correspond à la plage d'adresse que nous souhaitons extraire du fichier. On parcours ensuite la plage d'adresse du éseau et on liste toutes les différentes adresses attribuables afin de les retourner.

- associa_ip(mac): fonction qui prend en paramètre une adresse MAC et cherche dans le fichier de configuration si elle est associée à une adresse IP. Si oui nous retournons l'adresse IP en question sinon nous retournons 0.

- blacklist(mac): fonction qui prend en paramètre une adresse MAC et vérifie si elle fait partie des adresses MAC blacklistées dans le fichier de configuration.

===================================================================

Fonctions pour structurer les messages:

- get_offer(discover, addr=False): prends en paramètre le message discover reçu ainsi que l'adresse IP que nous devons proposer dans notre offer si il y en a une, sinon nous tirons une adresse aléatoire avec get_random_addr, et nous structurons notre message offer tel que souhaité en utilisant les fonctions de configurations. Nous retournons une liste contenant l'adresse proposé dans notre message ainsi que le message à envoyer.

- get_nack(r): prend en paramètre le message request reçu et retourne le message NAK correspondant à envoyer.

- get_ack(r, address): prend en paramètre le message request reçu ainsi que l'adresse IP que nous attribuons. Nous formons le message ACK comme souhaité avec les fonctions de configuration puis retournons le ACK à envoyer.

=====================================================================

Fonctions pour fichier historique:

- search_fic_line(mac, ip, id): fonction qui prend en paramètrre une adresse MAC, une adresse IP et un ID et cherhce si ces argument forment une ligne de l'historique. Retourne 1 si c'est le cas sinon retourne 0.

- search_fic_macip(mac, ip): fonction qui prend en paramètre une adresse MAC et une adresse IP et cherhce si ces adresses sont sur une même ligne de l'historique. Retourne 1 si c'est le cas sinon retourne 0.

- search_fic_mac(mac): fonction qui prend en paramètre une adresse MAC et regarde si elle est présente dans l'historique, si oui retourne l'adresse IP qui lui est associé sinon retourne 0.

- fic_offer(mac, ip, id): fonction qui prend en paramètrre une adresse MAC, une adresse IP et un ID et vérifie si l'adresse MAC est déjà présente dans l'historique, si oui modifie l'adresse IP et l'ID si ce n'est pas les bons sinon ajoute une ligne au fichier associant l'adresse MAC à son adresse IP et son ID.

=====================================================================

Fonctions pour efféctuer les pings:

- ping (ip) : Prend en paramètre un adresse IP sous la forme « x.x.x.x » (avec x compris entre 0 et 255) et envoie une requête ping à cette adresse. Si la station correspondant à l’adresse IP répond à la requête, on ajoute l’adresse IP à la liste « liste_ip ».

- thread_ip() : Soit une liste « list_addr » d’adresses IP appartenant à la plage d’adresses du serveur, pour lesquelles le serveur doit envoyer une requête « ping ». La fonction renvoie un tableau de threads pour la fonction ping(ip) pour chaque adresse IP de cette liste.

- thread_ip2() : Soit une liste « liste_ip » d’adresses IP déjà attribuées pour lesquelles le serveur doit envoyer une requête « ping ». La fonction renvoie un tableau de threads pour la fonction ping(ip) pour chaque adresse IP de cette liste.

=====================================================================

Fonctions autre:

- get_random_addr() : Retourne une adresse IP aléatoire appartenant à la plage d’adresses du serveur DHCP mais n’étant pas dans la liste « liste-ip » des adresses IP déjà attribuées par le serveur.

- extract_ip_req(r) : Prend en paramètre un message DHCPREQUEST et retourne l’adresse IP demandée par une station cliente.
- transf_into_mac(mac) : Prend en paramètre une adresse MAC en octets et le transforme en une adresse MAC en format hexadécimal.

- ajout_journal(s) : Prend en paramètre une chaîne de caractères et l’écrit dans le fichier « journal.txt ».

- verif_bail() : Grâce à un timer, envoie un ping toutes les x secondes à toutes les adresses IP déjà attribuées par le serveur de la liste « liste_ip ».

-create_win() : Crée une fenêtre de commandes de taille 500x300. Grâce à la fonction manage_command et en fonction des commandes entrées, affiche la liste des adresses IP déjà attribuées par le serveur (commande « ipocc »), la liste des adresses disponibles (commande « iplib ») et force l’arrêt du serveur DHCP (commande « quit »).


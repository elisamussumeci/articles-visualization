(function() {
  packages = {

    root: function (classes) {
      var map = {};

      // Para cada artigo, iremos criar as chaves que o D3 espera
      classes.forEach(function(d) {
        map[d._id['$oid']] = d;
        map[d._id['$oid']].key = d._id['$oid'];
        map[d._id['$oid']].name = d.title;
        map[d._id['$oid']].children = [];
        map[d._id['$oid']].parent = null;
      });

      // Como este visualização do D3 espera uma estrutura
      // hierarquica, criamos o nó raiz para que alguns sejam
      // filhos dele
      var root = {
        name: '',
        children: [],
        parent: null
      };

      // Agora, iremos criar um pai para cada hostname
      // e iremos colocar os filhos como aqueles que possuem
      // este hostname
      var hostnames = {};
      // Para cada artigo
      classes.forEach(function(d) {
        // Caso o hostname ja tenha sido criado
        if (hostnames[d.hostname]) {
          // Colocamos o artigo como filho
          hostnames[d.hostname].children.push(d);
        } else {
          // Criamos um hostname caso, ele ainda nao tenha
          // sido criado, colocamos o parent deste objeto
          // como o nó raiz e o artigo que o criou como
          // filho
          var newHostname = {
            name: d.hostname,
            key: "hostname",
            children: [d],
            parent: root
          };
          // Colocamos o hostname como filho do nó raiz
          root.children.push(newHostname);
          hostnames[d.hostname] = newHostname;
        }
        // Dizemos tambem, que o hostname é o seu pai
        d.parent = hostnames[d.hostname];
      });

      // Retornamos o nó raiz, já que ele tem acesso
      // a todos os outros nós
      return root;
    },

    imports: function (nodes) {
      var map = {},
          relation = [];

      // Criamos uma estrutura auxiliar
      nodes.forEach(function(d) {
        map[d.key] = d;
      });

      // Iremos linkar os artigos
      nodes.forEach(function(d) {
        if (d.key == "hostname")
          return;

        // Caso o artigo tenha alguma relação
        if (d.related) {
          for (var i = d.related.length - 1; i >= 0; i--) {
            // Pegamos o artigo relacionado
            var target = map[d.related[i]["$oid"]];
            // Fazemos o link
            relation.push({source: d, target: target});
          }
        }
      });

      return relation;
    }
  };
})();
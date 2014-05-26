(function() {
  packages = {

    root: function (classes) {
      var map = {};

      classes.forEach(function(d) {
        map[d._id['$oid']] = d;
        map[d._id['$oid']].key = d._id['$oid'];
        map[d._id['$oid']].name = d.title;
        map[d._id['$oid']].children = [];
        map[d._id['$oid']].parent = null;
      });

      var root = {
        name: '',
        children: [],
        parent: null
      };

      for (key in map) {
        var node = map[key];
        if (!node.parent) {
          root.children.push(node);
          node.parent = root;
        }
      }

      return root;
    },

    imports: function (nodes) {
      var map = {},
          relation = [];

      // Compute a map from name to node.
      nodes.forEach(function(d) {
        map[d.key] = d;
      });

      // For each import, construct a link from the source to target node.
      nodes.forEach(function(d) {
        if (d.childrenId) {
          for (var i = d.childrenId.length - 1; i >= 0; i--) {
            var children = map[d.childrenId[i]["$oid"]];
            relation.push({source: d, target: children});
          }
        }
      });

      return relation;
    }
  };
})();
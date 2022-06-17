th = treeHelper
app = new Vue({
  el: '#edit_funnel_app',
  components: {Tree: vueDraggableNestedTree.DraggableTree},
  data: {
    tree1data: [
        {text: 'node 1'},
        {text: 'node 2'},
        {text: 'node 3 undraggable', draggable: false},
        {text: 'node 4'},
        {text: 'node 4 undroppable', droppable: false},
        {text: 'node 5', children: [
          {text: 'node 1'},
          {text: 'node 2', children: [
            {text: 'node 3'},
            {text: 'node 4'},
          ]},
          {text: 'node 2 undroppable', droppable: false, children: [
            {text: 'node 3'},
            {text: 'node 4'},
          ]},
          {text: 'node 2', children: [
            {text: 'node 3'},
            {text: 'node 4 undroppable', droppable: false},
          ]},
          {text: 'node 3'},
          {text: 'node 4'},
          {text: 'node 3'},
          {text: 'node 4'},
          {text: 'node 3'},
          {text: 'node 4'},
          {text: 'node 3'},
          {text: 'node 4'},
        ]},
      ],

  },
  methods: {
    // add child to tree2
    addChild() {
      this.tree2data[0].children.push({text: 'child'})
    },
    expandAll() {
      th.breadthFirstSearch(this.tree1data, node => {
        node.open = true
      })
    },
    collapseAll() {
      th.breadthFirstSearch(this.tree1data, node => {
        node.open = false
      })
    },
  },
})
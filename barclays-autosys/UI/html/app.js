function init() {
    if (window.goSamples) goSamples();  // init for these samples -- you don't need to call this
    var $ = go.GraphObject.make;  // for conciseness in defining templates

    myDiagram =
      $(go.Diagram, "myDiagramDiv",  // create a Diagram for the DIV HTML element
        {
          // position the graph in the middle of the diagram
          initialContentAlignment: go.Spot.Center,

          // allow double-click in background to create a new node
          // "clickCreatingTool.archetypeNodeData": { text: "Node", color: "white" },
// 
          // allow Ctrl-G to call groupSelection()
          "commandHandler.archetypeGroupData": { text: "Group", isGroup: true, color: "blue" },

          // enable undo & redo
          "undoManager.isEnabled": true
        });




  function showMessage(s, b) {
    jQuery("#sidePanel").removeClass('hidden').addClass('col-md-3').addClass("col-sm-3");
    jQuery("#myDiagramDiv").removeClass("col-md-12").removeClass("col-sm-12").addClass("col-md-9").addClass("col-sm-9")

    // document.getElementById("diagramEventsMsg").textContent = s;
    document.getElementById("diagramEventsMsg_Node").textContent = b.key;
    console.log(b);
    jQuery("#saveBtn").attr("data-key", b.key);
    if (!b.status) b.status = "completed" 
    jQuery("#saveBtn").attr("data-status", b.status)
    jQuery("#saveBtn").attr("data-time", b.time);
    var type;

    if (b.isGroup){
      jQuery("#side-panel-body").addClass('hidden')
      jQuery("#side-panel-footer").addClass('hidden')
      type = "Box"
    } else {
      jQuery("#side-panel-body").removeClass('hidden')
      jQuery("#side-panel-footer").removeClass('hidden')
      type = "Job"
    }

    document.getElementById("jobType").textContent = (type + " Name:")
  }
  
  myDiagram.addDiagramListener("ObjectSingleClicked",
      function(e) {
        var part = e.subject.part;
        if (!(part instanceof go.Link)) showMessage("Clicked on ", part.data);
      });
    // Define the appearance and behavior for Nodes:

    // First, define the shared context menu for all Nodes, Links, and Groups.

    // To simplify this code we define a function for creating a context menu button:
    function makeButton(text, action, visiblePredicate) {
      return $("ContextMenuButton",
               $(go.TextBlock, text),
               { click: action },
               // don't bother with binding GraphObject.visible if there's no predicate
               visiblePredicate ? new go.Binding("visible", "", visiblePredicate).ofObject() : {});
    }
    // myDiagram.isReadOnly = true;
    // a context menu is an Adornment with a bunch of buttons in them
    var partContextMenu =
      $(go.Adornment, "Vertical",
          makeButton("Properties",
                     function(e, obj) {  // OBJ is this Button
                       var contextmenu = obj.part;  // the Button is in the context menu Adornment
                       var part = contextmenu.adornedPart;  // the adornedPart is the Part that the context menu adorns
                       // now can do something with PART, or with its data, or with the Adornment (the context menu)
                       if (part instanceof go.Link) alert(linkInfo(part.data));
                       else if (part instanceof go.Group) alert(groupInfo(contextmenu));
                       else alert(nodeInfo(part.data));
                     }),
          makeButton("Cut",
                     function(e, obj) { e.diagram.commandHandler.cutSelection(); },
                     function(o) { return o.diagram.commandHandler.canCutSelection(); }),
          makeButton("Copy",
                     function(e, obj) { e.diagram.commandHandler.copySelection(); },
                     function(o) { return o.diagram.commandHandler.canCopySelection(); }),
          makeButton("Paste",
                     function(e, obj) { e.diagram.commandHandler.pasteSelection(e.diagram.lastInput.documentPoint); },
                     function(o) { return o.diagram.commandHandler.canPasteSelection(); }),
          makeButton("Delete",
                     function(e, obj) { e.diagram.commandHandler.deleteSelection(); },
                     function(o) { return o.diagram.commandHandler.canDeleteSelection(); }),
          makeButton("Undo",
                     function(e, obj) { e.diagram.commandHandler.undo(); },
                     function(o) { return o.diagram.commandHandler.canUndo(); }),
          makeButton("Redo",
                     function(e, obj) { e.diagram.commandHandler.redo(); },
                     function(o) { return o.diagram.commandHandler.canRedo(); }),
          makeButton("Group",
                     function(e, obj) { e.diagram.commandHandler.groupSelection(); },
                     function(o) { return o.diagram.commandHandler.canGroupSelection(); }),
          makeButton("Ungroup",
                     function(e, obj) { e.diagram.commandHandler.ungroupSelection(); },
                     function(o) { return o.diagram.commandHandler.canUngroupSelection(); })
      );


    function nodeInfo(d) {  // Tooltip info for a node data object
      var str = "Node " + d.key + ": " + d.text + "\n";
      if (d.group)
        str += "member of " + d.group;
      else
        str += "top-level node";
      return str;
    }

function incrementCounter(e, obj) {
    var node = obj.part;
    var data = node.data;
    if (data) {
      node.diagram.startTransaction("clicked");
      var old = data.clickCount;
      data.clickCount++;
      node.diagram.model.raiseDataChanged(data, "clickCount", old, data.clickCount);
      node.diagram.commitTransaction("clicked");
    }
  }
    // These nodes have text surrounded by a rounded rectangle
    // whose fill color is bound to the node data.
    // The user can drag a node by dragging its TextBlock label.
    // Dragging from the Shape will start drawing a new link.
    myDiagram.nodeTemplate =
      $(go.Node, "Auto",
        { locationSpot: go.Spot.Center },
        $(go.Shape, "RoundedRectangle",
          {
            fill: "white", // the default fill, if there is no data-binding
            portId: "", cursor: "pointer",  // the Shape is the port, not the whole Node
            // allow all kinds of links from and to this port
            fromLinkable: true, fromLinkableSelfNode: true, fromLinkableDuplicates: true,
            toLinkable: true, toLinkableSelfNode: true, toLinkableDuplicates: true
          },
          new go.Binding("fill", "color")),
        $(go.Panel, "Spot",
        new go.Binding("opacity", "status", function(t) { return t ? 1 : 0; }),
        // note that the opacity defaults to zero (not visible),
        // in case there is no "ribbon" property
        { opacity: 0.7,
          alignment: new go.Spot(1, 0, 5, -5),
          alignmentFocus: go.Spot.TopRight },
        $(go.Shape,  // the ribbon itself
          { geometryString: "F1 M0 0 L30 0 70 40 70 70z",
            fill: "red", stroke: null, strokeWidth: 0 }),
        $(go.TextBlock,
          new go.Binding("text", "status"),
          { alignment: new go.Spot(1, 0, -29, 29),
            angle: 45, maxSize: new go.Size(100, NaN),
            stroke: "white", font: "bold 10px sans-serif", textAlign: "center" })
      ),
        $(go.Panel, "Table",
          { defaultAlignment: go.Spot.Left },
          $(go.TextBlock, { row: 3, column: 0, columnSpan: 2, alignment: go.Spot.Center,  font: "bold 12pt sans-serif" },
            new go.Binding("text", "text").makeTwoWay()),
          $(go.TextBlock, { row: 0, column: 0, columnSpan:2 }, ""),
          $(go.TextBlock, { row: 1, column: 0, columnSpan:2 }, ""),
          $(go.TextBlock, { row: 2, column: 0, columnSpan:2 }, ""),

          $(go.TextBlock, { row: 4, column: 0 }, "Average Run Time:"),
          $(go.TextBlock, { row: 4, column: 1 }, new go.Binding("text", "default")),
          $(go.TextBlock, { row: 5, column: 0 }, new go.Binding("text", "status", getStatus)),
          $(go.TextBlock, { row: 5, column: 1 }, new go.Binding("text", "time")),
          $(go.TextBlock, { row: 6, column: 0 }, "Ends At"),
          $(go.TextBlock, { row: 6, column: 1 }, new go.Binding("text", "cum")),
          // $(go.TextBlock, { row: 3, column: 0 }, "Documentation:"),
          $(go.TextBlock, { row: 7, column: 0, alignment: go.Spot.Center, columnSpan: 2, font: "bold 7pt sans-serif" , click: function(e, obj) {window.open(obj.part.data.url)}}, "Documentation")
          // $(go.TextBlock, { row: 2, column: 0 }, "Color:"),
          // $(go.TextBlock, { row: 2, column: 1 }, new go.Binding("text", "color"))
        )
      );

    // Define the appearance and behavior for Links:
    function getStatus(status){
      // var status = content.content
      // console.log(content);
      console.log(status)
      if (status == "completed") {
        var out = "Last Run Time:"
      } else {
        var out = "Predicted Run Time:"
      }

      return out
    }

    function linkInfo(d) {  // Tooltip info for a link data object
      return "Link:\nfrom " + d.from + " to " + d.to;
    }

    // The link shape and arrowhead have their stroke brush data bound to the "color" property
    myDiagram.linkTemplate =
      $(go.Link,
        { toShortLength: 3, relinkableFrom: true, relinkableTo: true },  // allow the user to relink existing links
        $(go.Shape,
          { strokeWidth: 2 },
          new go.Binding("stroke", "color")),
        $(go.Shape,
          { toArrow: "Standard", stroke: null },
          new go.Binding("fill", "color")),
        { // this tooltip Adornment is shared by all links
          toolTip:
            $(go.Adornment, "Auto",
              $(go.Shape, { fill: "hsl(70, 100%, 100%)" }),
              $(go.TextBlock, { margin: 4 },  // the tooltip shows the result of calling linkInfo(data)
                new go.Binding("text", "", linkInfo))
            ),
          // the same context menu Adornment is shared by all links
          contextMenu: partContextMenu
        }
      );

    // Define the appearance and behavior for Groups:

    function groupInfo(adornment) {  // takes the tooltip or context menu, not a group node data object
      var g = adornment.adornedPart;  // get the Group that the tooltip adorns
      var mems = g.memberParts.count;
      var links = 0;
      g.memberParts.each(function(part) {
        if (part instanceof go.Link) links++;
      });
      return "Group " + g.data.key + ": " + g.data.text + "\n" + mems + " members including " + links + " links";
    }

    // Groups consist of a title in the color given by the group node data
    // above a translucent gray rectangle surrounding the member parts
    myDiagram.groupTemplate =
      $(go.Group, "Vertical",
        { selectionObjectName: "PANEL",  // selection handle goes around shape, not label
          ungroupable: true },  // enable Ctrl-Shift-G to ungroup a selected Group
        $(go.TextBlock,
          {
            font: "bold 19px sans-serif",
            isMultiline: false,  // don't allow newlines in text
            editable: true  // allow in-place editing by user
          },
          new go.Binding("text", "text").makeTwoWay(),
          new go.Binding("stroke", "color")),
        $(go.Panel, "Auto",
          { name: "PANEL" },
          $(go.Shape, "RoundedRectangle",  // the rectangular shape around the members
            { fill: "#D3D3D3", stroke: "black", strokeWidth: 3 }),
          $(go.Placeholder, { padding: 10 })  // represents where the members are
        ),
        $(go.Panel, "Horizontal",  // the header
          { defaultAlignment: go.Spot.Top },
          $("SubGraphExpanderButton"),  // this Panel acts as a Button
          $(go.TextBlock,     // group title near top, next to button
            { font: "Bold 12pt Sans-Serif" },
            new go.Binding("text", "key")),
          $(go.Panel, "Table",
          { defaultAlignment: go.Spot.Left },
          $(go.TextBlock, { row: 0, column: 0, columnSpan: 2, alignment: go.Spot.Center,  font: "bold 12pt sans-serif" },
            new go.Binding("text", "text").makeTwoWay()),
          $(go.TextBlock, { row: 1, column: 0 }, "Expected Run Time:"),
          $(go.TextBlock, { row: 1, column: 1 }, new go.Binding("text", "default")),
          $(go.TextBlock, { row: 2, column: 0 }, "Last Run Time:"),
          $(go.TextBlock, { row: 2, column: 1 }, new go.Binding("text", "time")),
          $(go.TextBlock, { row: 6, column: 0 }, "Ends At"),
          $(go.TextBlock, { row: 6, column: 1 }, new go.Binding("text", "cum"))
          // $(go.TextBlock, { row: 3, column: 0 }, "Documentation:"),
          // $(go.TextBlock, { row: 3, column: 0, alignment: go.Spot.Center, columnSpan: 2, font: "bold 7pt sans-serif" , click: function(e, obj) {window.open(obj.part.data.url)}}, "Documentation Here")
          // $(go.TextBlock, { row: 2, column: 0 }, "Color:"),
          // $(go.TextBlock, { row: 2, column: 1 }, new go.Binding("text", "color"))
        )
        ),
        { // this tooltip Adornment is shared by all groups
          toolTip:
            $(go.Adornment, "Auto",
              $(go.Shape, { fill: "#FFFFCC" }),
              $(go.TextBlock, { margin: 4 },
                // bind to tooltip, not to Group.data, to allow access to Group properties
                new go.Binding("text", "", groupInfo).ofObject())
            ),
          // the same context menu Adornment is shared by all groups
          contextMenu: partContextMenu
        }
      );

    // Define the behavior for the Diagram background:

    function diagramInfo(model) {  // Tooltip info for the diagram's model
      return "Model:\n" + model.nodeDataArray.length + " nodes, " + model.linkDataArray.length + " links";
    }

    // provide a tooltip for the background of the Diagram, when not over any Part
    myDiagram.toolTip =
      $(go.Adornment, "Auto",
        $(go.Shape, { fill: "#FFFFCC" }),
        $(go.TextBlock, { margin: 4 },
          new go.Binding("text", "", diagramInfo))
      );

    // provide a context menu for the background of the Diagram, when not over any Part
    myDiagram.contextMenu =
      $(go.Adornment, "Vertical",
          makeButton("Paste",
                     function(e, obj) { e.diagram.commandHandler.pasteSelection(e.diagram.lastInput.documentPoint); },
                     function(o) { return o.diagram.commandHandler.canPasteSelection(); }),
          makeButton("Undo",
                     function(e, obj) { e.diagram.commandHandler.undo(); },
                     function(o) { return o.diagram.commandHandler.canUndo(); }),
          makeButton("Redo",
                     function(e, obj) { e.diagram.commandHandler.redo(); },
                     function(o) { return o.diagram.commandHandler.canRedo(); })
      );

    // Create the Diagram's Model:
    jQuery.get("http://localhost:8000/nodes", function(data) {
      var nodeDataArray = data.nodes;
      /*var nodeDataArray = [
      { 'key': 1, text: "Job 3" },
      { 'key': 2, text: "Job 4", color: "orange" },
      { 'key': 3, text: "Job 1", color: "lightgreen", group: 'b5' },
      { key: 4, text: "Job 2", color: "pink", group: 'b5' },
      { key: 'b5', text: "Box 1", color: "green", isGroup: true }
    ];*/
      jQuery.get("http://localhost:8000/links", function(data) {

        var linkDataArray = data.links;
        myDiagram.model = new go.GraphLinksModel(nodeDataArray, linkDataArray);
      
        jQuery.get("http://localhost:8000/time_details", function(data) {
          var timings = data.times
          var start_time = timings.start_time
          var end_time_pred = timings.end_time_pred
          var end_time_target = timings.end_time_target
          // console.log(start_time)

          document.getElementById("display").textContent = "Started At: " + start_time + " | Predicted End Time: " + end_time_pred +  " | Avg. End Time: " + end_time_target;

        });
      });


    });


    jQuery("#saveBtn").on("click", function() {
      // console.log('hello')
        var SLA = parseFloat(jQuery("#SLA").val())
        var Comp_Time = jQuery("CompletionTime").val()
        var key = jQuery(this).attr("data-key");
        var time = parseFloat(jQuery(this).attr("data-time"))
        // console.log(key)
        var data = myDiagram.model.findNodeDataForKey(key);
        var url = jQuery("#url").val()
        var status = jQuery(this).attr("data-status")

        // console.log(status)
        // This will update the color of the "Delta" Node
        var color = getColor(time ,SLA, status)

        if (!!SLA){
            if (data !== null) myDiagram.model.setDataProperty(data, "color", color);
            if (data !== null) myDiagram.model.setDataProperty(data, "default", SLA);
        }
        if (!! url) if (data !== null) myDiagram.model.setDataProperty(data, "url", url);

        // var node = document.getElementById("diagramEventsMsg_Node").textContent

        alert("Saved Changes!")
    });


    
  }

function hsv2rgb(h, s, v) {
  // var h = hsv.hue, s = hsv.sat, v = hsv.val;
  var rgb, i, data = [];
  if (s === 0) {
    rgb = [v,v,v];
  } else {
    h = h / 60;
    i = Math.floor(h);
    data = [v*(1-s), v*(1-s*(h-i)), v*(1-s*(1-(h-i)))];
    switch(i) {
      case 0:
        rgb = [v, data[2], data[0]];
        break;
      case 1:
        rgb = [data[1], v, data[0]];
        break;
      case 2:
        rgb = [data[0], v, data[2]];
        break;
      case 3:
        rgb = [data[0], data[1], v];
        break;
      case 4:
        rgb = [data[2], data[0], v];
        break;
      default:
        rgb = [v, data[0], data[1]];
        break;
    }
  }
  return '#' + rgb.map(function(x){ 
    return ("0" + Math.round(x*255).toString(16)).slice(-2);
  }).join('');
};

function getColor(current, threshold, status){

  var sat = 1;
  if (status == "incomplete") sat = 0
  var val = 60.0 + 90*(threshold-current)/threshold
  if (val < 0) val = 0
  else if (val > 120) val = 120 
  var color = hsv2rgb(val, sat, 1)
  return color
}



function change(e, obj){
      // OBJ is this Button
   var contextmenu = obj.part;  // the Button is in the context menu Adornment
   var part = contextmenu.adornedPart;  // the adornedPart is the Part that the context menu adorns
   // now can do something with PART, or with its data, or with the Adornment (the context menu)
   if (part instanceof go.Link) alert(linkInfo(part.data));
   else if (part instanceof go.Group) alert(groupInfo(contextmenu));
   else alert(nodeInfo(part.data));

}


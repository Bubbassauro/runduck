(this["webpackJsonprunduck-ui"]=this["webpackJsonprunduck-ui"]||[]).push([[0],{362:function(e,t,a){e.exports=a(454)},367:function(e,t,a){},454:function(e,t,a){"use strict";a.r(t);var n=a(0),r=a.n(n),o=a(16),c=a.n(o),i=(a(367),a(27)),l=a(28),u=a(29),s=a(30),m=a(343),p=a.n(m),d=a(232),h=a(326),f=a(479),b=a(483),v=a(354),E=a.n(v),y=a(331),g=a(308),j=a(85),O=a(350),k=a.n(O),x=function(e){Object(s.a)(a,e);var t=Object(u.a)(a);function a(){return Object(i.a)(this,a),t.apply(this,arguments)}return Object(l.a)(a,[{key:"render",value:function(){return r.a.createElement(d.a,null,r.a.createElement(j.a,{color:"textSecondary"},r.a.createElement(g.a,{title:"exec"},r.a.createElement(k.a,{fontSize:"small",style:{marginRight:"5px",marginBottom:"-5px"}})),this.props.command.description),r.a.createElement(j.a,{variant:"body2",style:{whiteSpace:"pre-line"}},r.a.createElement("code",null,this.props.command.exec)))}}]),a}(n.Component),S=a(351),C=a.n(S),w=function(e){Object(s.a)(a,e);var t=Object(u.a)(a);function a(){return Object(i.a)(this,a),t.apply(this,arguments)}return Object(l.a)(a,[{key:"render",value:function(){var e=this.props.command.jobref;return r.a.createElement(d.a,null,r.a.createElement(j.a,{color:"textSecondary"},r.a.createElement(g.a,{title:"jobref"},r.a.createElement(C.a,{fontSize:"small",style:{marginRight:"5px",marginBottom:"-5px"}})),null===e||void 0===e?void 0:e.project," ",(null===e||void 0===e?void 0:e.group)?"/ ".concat(e.group):""),r.a.createElement(j.a,{variant:"subtitle1"},null===e||void 0===e?void 0:e.name))}}]),a}(n.Component),R=a(352),D=a.n(R),B=function(e){Object(s.a)(a,e);var t=Object(u.a)(a);function a(){return Object(i.a)(this,a),t.apply(this,arguments)}return Object(l.a)(a,[{key:"render",value:function(){var e,t;return r.a.createElement(d.a,null,r.a.createElement(j.a,{color:"textSecondary"},r.a.createElement(g.a,{title:"configuration"},r.a.createElement(D.a,{fontSize:"small",style:{marginRight:"5px",marginBottom:"-5px"}})),null===(e=this.props.command)||void 0===e?void 0:e.type),r.a.createElement(j.a,{variant:"body2",style:{whiteSpace:"pre-line"}},r.a.createElement("code",null,null===(t=this.props.command.configuration)||void 0===t?void 0:t.command)))}}]),a}(n.Component),J=a(353),T=a.n(J),_=function(e){Object(s.a)(a,e);var t=Object(u.a)(a);function a(){return Object(i.a)(this,a),t.apply(this,arguments)}return Object(l.a)(a,[{key:"render",value:function(){return r.a.createElement(d.a,null,r.a.createElement(j.a,{color:"textSecondary"},r.a.createElement(g.a,{title:"script"},r.a.createElement(T.a,{fontSize:"small",style:{marginRight:"5px",marginBottom:"-5px"}})),this.props.command.description),r.a.createElement(j.a,{variant:"body2",style:{whiteSpace:"pre-line"}},r.a.createElement("code",null,this.props.command.script)))}}]),a}(n.Component),z=function(e){Object(s.a)(a,e);var t=Object(u.a)(a);function a(){return Object(i.a)(this,a),t.apply(this,arguments)}return Object(l.a)(a,[{key:"render",value:function(){var e;return e=this.props.command.jobref?r.a.createElement(w,{command:this.props.command}):this.props.command.exec?r.a.createElement(x,{command:this.props.command}):this.props.command.configuration?r.a.createElement(B,{command:this.props.command}):r.a.createElement(_,{command:this.props.command}),r.a.createElement(d.a,{my:2},e)}}]),a}(n.Component),W=a(183),I=function(e){Object(s.a)(a,e);var t=Object(u.a)(a);function a(){return Object(i.a)(this,a),t.apply(this,arguments)}return Object(l.a)(a,[{key:"render",value:function(){return r.a.createElement(d.a,null,r.a.createElement(j.a,{variant:"subtitle1"},this.props.title),r.a.createElement(j.a,{variant:"subtitle2",color:"textSecondary"},this.props.email.subject," "),r.a.createElement(j.a,{variant:"body2"},this.props.email.recipients," "))}}]),a}(n.Component),M=function(e){Object(s.a)(a,e);var t=Object(u.a)(a);function a(){return Object(i.a)(this,a),t.apply(this,arguments)}return Object(l.a)(a,[{key:"render",value:function(){var e,t;return this.props.notification&&(this.props.notification.onsuccess&&(e=r.a.createElement(I,{email:this.props.notification.onsuccess.email,title:"On Success"})),this.props.notification.onfailure&&(t=r.a.createElement(I,{email:this.props.notification.onfailure.email,title:"On Failure"}))),r.a.createElement(d.a,null,this.props.notification?r.a.createElement(f.a,{container:!0,spacing:2,alignItems:"stretch"},e?r.a.createElement(f.a,{item:!0,xs:!0},r.a.createElement(W.a,{style:{height:"100%",padding:"1em"}},e)):"",t?r.a.createElement(f.a,{item:!0,xs:!0},r.a.createElement(W.a,{style:{height:"100%",padding:"1em"}},t)):""):"")}}]),a}(n.Component);function A(e){var t=document.getElementById("public_url");return console.log({public_url:t.value}),t&&t.value?"".concat(t.value,"/").concat(e):"http://localhost:3825/".concat(e)}var L=function(e){Object(s.a)(a,e);var t=Object(u.a)(a);function a(){var e;Object(i.a)(this,a);for(var n=arguments.length,r=new Array(n),o=0;o<n;o++)r[o]=arguments[o];return(e=t.call.apply(t,[this].concat(r))).state={description:"-",name:"",permalink:"",commands:[],notification:{},updated:""},e}return Object(l.a)(a,[{key:"getUpdatedStr",value:function(e){if(e){var t=new Date(e);return"Last Updated: ".concat(t.toString())}return""}},{key:"loadJobData",value:function(){var e=this,t=arguments.length>0&&void 0!==arguments[0]&&arguments[0],a=this.props.data.env,n=this.props.data.uuid,r="api/job/".concat(a,"/").concat(n,"?force_refresh=").concat(t),o=A(r);fetch(o).then((function(e){return e.json()})).then((function(t){e.setState({name:t.name,permalink:t.permalink,description:t.description,commands:t.sequence?t.sequence.commands:[],notification:t.notification,updated:e.getUpdatedStr(t.updated)})})).catch(console.log)}},{key:"componentDidMount",value:function(){this.loadJobData()}},{key:"render",value:function(){var e=this;return r.a.createElement(d.a,{pl:6,p:2,style:{backgroundColor:this.props.theme.palette.background.default}},r.a.createElement(f.a,{container:!0},r.a.createElement(f.a,{item:!0,style:{flex:1}},r.a.createElement(b.a,{variant:"h6",href:this.state.permalink,color:"textPrimary",target:"_blank"},this.state.name)),r.a.createElement(f.a,{item:!0},r.a.createElement(j.a,{noWrap:!0,variant:"body2",color:"textSecondary"},this.state.updated,"\xa0\xa0",r.a.createElement(h.a,{variant:"contained",size:"small",startIcon:r.a.createElement(E.a,null),onClick:function(){return e.loadJobData(!0)}},"Refresh")))),this.state.commands.map((function(e,t){return r.a.createElement(d.a,{key:t},r.a.createElement(z,{command:e}))})),r.a.createElement(M,{notification:this.state.notification}))}}]),a}(n.Component),P=Object(y.a)(L),U=a(340),q=a(198),G=a.n(q),N=a(197),F=a.n(N),H=a(246),$=a.n(H),K=a(196),Q=a.n(K),V=a(245),X=a.n(V),Y=a(195),Z=a.n(Y);function ee(e,t){switch(t){case 0:return{backgroundColor:G.a[300],color:e.palette.getContrastText(G.a[300])};case 1:return{backgroundColor:F.a[300],color:e.palette.getContrastText(F.a[300])};case 2:return{backgroundColor:Q.a[300],color:e.palette.getContrastText(Q.a[300])};case 3:return{backgroundColor:X.a[300],color:e.palette.getContrastText(X.a[300])};case 4:return{backgroundColor:Z.a[300],color:e.palette.getContrastText(Z.a[300])};case 5:return{backgroundColor:$.a[300],color:e.palette.getContrastText($.a[300])};default:return{backgroundColor:e.palette.background.default,color:e.palette.getContrastText(e.palette.background.default)}}}var te=function(e){Object(s.a)(a,e);var t=Object(u.a)(a);function a(){return Object(i.a)(this,a),t.apply(this,arguments)}return Object(l.a)(a,[{key:"render",value:function(){return r.a.createElement(U.a,{size:"small",label:this.props.label,style:ee(this.props.theme,this.props.index)})}}]),a}(n.Component),ae=Object(y.a)(te);function ne(e,t){var a=new Set(e.map((function(e){return e[t]}))),n={};return a.forEach((function(e){n[e]=e})),n}var re=function(e){Object(s.a)(a,e);var t=Object(u.a)(a);function a(){var e;Object(i.a)(this,a);for(var n=arguments.length,o=new Array(n),c=0;c<n;c++)o[c]=arguments[c];return(e=t.call.apply(t,[this].concat(o))).tableRef=r.a.createRef(),e.colRenderCount=0,e.state={data:[],environments:{}},e}return Object(l.a)(a,[{key:"componentDidMount",value:function(){var e=this;fetch(A("api/jobs")).then((function(e){return e.json()})).then((function(t){e.setState({data:t.data,environments:ne(t.data,"env")})})).catch(console.log)}},{key:"getDetails",value:function(e){return r.a.createElement(P,{data:e})}},{key:"render",value:function(){var e=this;return r.a.createElement("div",null,r.a.createElement("div",{style:{maxWidth:"100%"}},r.a.createElement(p.a,{options:{paging:!1,grouping:!0,filtering:!0,tableLayout:"fixed",padding:"dense",headerStyle:{position:"sticky",top:0},maxBodyHeight:"calc(100vh - 127px)",rowStyle:function(t){return{color:(a=t,a.scheduleEnabled&&a.executionEnabled?e.props.theme.palette.text.primary:e.props.theme.palette.text.disabled)};var a}},columns:[{title:"Project",field:"project_name",width:"12em",defaultGroupOrder:0},{title:"Group",field:"group",width:"15em",cellStyle:{paddingLeft:"50px"}},{title:"Environment",field:"env",width:"7em",lookup:this.state.environments,render:function(e){return r.a.createElement(ae,{label:e.env,index:e.env_order})}},{title:"Job Name",field:"name",width:"30%",cellStyle:{fontWeight:"bold"}},{title:"Schedule",field:"schedule_description",width:"15em"},{title:"Schedule Enabled",field:"scheduleEnabled",type:"boolean",width:"6em"},{title:"Execution Enabled",field:"executionEnabled",type:"boolean",width:"6em"},{title:"Description",field:"description",width:"40%",cellStyle:{whiteSpace:"pre-line"}}],data:this.state.data,detailPanel:function(t){return e.getDetails(t)},onRowClick:function(e,t,a){a&&a()},title:r.a.createElement(d.a,null,r.a.createElement(j.a,{variant:"h6",component:"span"},"Runduck"),r.a.createElement(j.a,{variant:"body2",color:"textSecondary",component:"span"},"\xa0\xa0\xa0\xa0Jobs from multiple Rundecks"))})))}}]),a}(n.Component),oe=Object(y.a)(re),ce=a(469),ie=a(175),le=a(481),ue=a(482);var se=function(){var e=Object(ce.a)("(prefers-color-scheme: dark)"),t=r.a.useMemo((function(){return Object(ie.a)({palette:{type:e?"dark":"light"}})}),[e]);return r.a.createElement(le.a,{theme:t},r.a.createElement(ue.a,null),r.a.createElement("div",{className:"App"},r.a.createElement(oe,null)))};Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));c.a.render(r.a.createElement(r.a.StrictMode,null,r.a.createElement(se,null)),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()})).catch((function(e){console.error(e.message)}))}},[[362,1,2]]]);
//# sourceMappingURL=main.e1613fa1.chunk.js.map
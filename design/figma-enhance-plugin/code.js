// Adds reusable HKchat components and interactive prototype links to the editable screens.
const P = {
  dark:'#301542', accent:'#A81C7F', pink:'#F553AB', pale:'#FFD1E9',
  text:'#37213F', muted:'#796B82', border:'#EADCEB', input:'#F9F5F9',
  bubble:'#F7F2F7', white:'#FFFFFF', danger:'#B42318', canvas:'#F4EFF5'
};
const F = {regular:{family:'Inter',style:'Regular'}, bold:{family:'Inter',style:'Bold'}};
function rgb(h){h=h.replace('#','');return {r:parseInt(h.slice(0,2),16)/255,g:parseInt(h.slice(2,4),16)/255,b:parseInt(h.slice(4,6),16)/255};}
function fill(hex){return [{type:'SOLID',color:rgb(hex)}];}
function rect(parent,name,x,y,w,h,color,r=0,stroke){
  const n=figma.createRectangle();n.name=name;n.resize(w,h);n.x=x;n.y=y;n.cornerRadius=r;n.fills=fill(color);
  if(stroke){n.strokes=fill(stroke);n.strokeWeight=1;}
  parent.appendChild(n);return n;
}
function text(parent,name,value,x,y,w,h,size=16,color=P.text,bold=false){
  const n=figma.createText();parent.appendChild(n);n.name=name;n.fontName=bold?F.bold:F.regular;
  n.fontSize=size;n.fills=fill(color);n.characters=value;n.resize(w,h);n.x=x;n.y=y;
  n.textAlignVertical='CENTER';return n;
}
function component(parent,name,x,y,w,h,color,label,labelColor=P.white){
  const c=figma.createComponent();parent.appendChild(c);c.name=name;c.resize(w,h);c.x=x;c.y=y;
  c.fills=fill(color);c.cornerRadius=12;
  const t=text(c,'Nhãn',label,0,0,w,h,15,labelColor,true);t.textAlignHorizontal='CENTER';
  return c;
}
function setVariants(parent,title,spec,x,y,w=230,h=44){
  const nodes=spec.map(([state,color,label,labelColor],i)=>component(parent,'State='+state,x+i*(w+24),y,w,h,color,label,labelColor));
  const set=figma.combineAsVariants(nodes,parent);set.name=title;set.x=x;set.y=y;return set;
}
async function designSystem(){
  let page=figma.root.children.find(p=>p.type==='PAGE'&&p.name==='HKchat – Design System');
  if(page){await figma.setCurrentPageAsync(page);await page.loadAsync();if(page.children.length)return page;}
  else{page=figma.createPage();page.name='HKchat – Design System';await figma.setCurrentPageAsync(page);}
  const board=figma.createFrame();page.appendChild(board);board.name='HKchat / Design System';board.resize(1300,1880);board.fills=fill(P.white);
  text(board,'Tiêu đề','HKchat  /  Design System',50,40,1120,50,32,P.dark,true);
  text(board,'Mô tả','Thành phần tái sử dụng cho giao diện nhắn tin nội bộ',50,91,1120,28,16,P.muted);
  text(board,'Mục màu','01  Màu sắc',50,148,900,36,24,P.dark,true);
  const colors=[['Nền đậm',P.dark],['Nhấn',P.accent],['Hồng',P.pink],['Hồng nhạt',P.pale],['Chữ',P.text],['Viền',P.border],['Nền input',P.input],['Xóa',P.danger]];
  colors.forEach(([label,hex],i)=>{let x=50+(i%4)*295,y=205+Math.floor(i/4)*112;rect(board,'Màu / '+label,x,y,260,58,hex,10);text(board,'Mã màu / '+label,label+'  '+hex,x,y+62,260,28,13,P.text);});
  text(board,'Mục chữ','02  Typography',50,455,900,36,24,P.dark,true);
  text(board,'Heading','Tiêu đề màn hình',50,504,550,48,28,P.dark,true);
  text(board,'Body','Nội dung hội thoại và mô tả sản phẩm',50,554,800,34,16,P.text);
  text(board,'Label','Nhãn, trạng thái và chú thích',50,592,800,27,13,P.muted);
  text(board,'Mục khoảng cách','03  Layout và spacing',50,654,900,36,24,P.dark,true);
  text(board,'Giá trị spacing','Lưới cơ sở 8 px   ·   Khoảng cách 8 / 16 / 24 / 32 px   ·   Frame 390 × 844 px',50,698,1120,33,15,P.text);
  [8,16,24,32].forEach((v,i)=>{let x=50+i*150;rect(board,'Spacing '+v,x,743,v*3,25,P.pink,4);text(board,'Nhãn '+v,v+' px',x,775,110,25,13,P.muted);});
  text(board,'Mục thành phần','04  Components và variants',50,839,900,36,24,P.dark,true);
  text(board,'Nhãn nút','Button',50,887,900,27,18,P.dark,true);
  setVariants(board,'Button / State',[
    ['Primary',P.accent,'Tiếp tục',P.white],
    ['Secondary',P.pale,'Hủy',P.text],
    ['Disabled',P.border,'Tiếp tục',P.muted],
    ['Destructive',P.danger,'Xóa',P.white]
  ],50,925,230,44);
  text(board,'Nhãn input','Input',50,1043,900,27,18,P.dark,true);
  const inputs=[
    ['Default',P.input,P.border,'Nhập nội dung',P.muted],
    ['Focused',P.white,P.accent,'Nội dung đang nhập',P.text],
    ['Error',P.white,P.danger,'Vui lòng kiểm tra',P.danger]
  ].map(([state,bg,border,label,color],i)=>{
    const c=figma.createComponent();board.appendChild(c);c.name='State='+state;c.resize(315,52);c.x=50+i*378;c.y=1082;c.fills=fill(bg);c.cornerRadius=12;c.strokes=fill(border);c.strokeWeight=2;
    text(c,'Nội dung',label,15,4,280,44,14,color);return c;
  });
  const inputSet=figma.combineAsVariants(inputs,board);inputSet.name='Input / State';inputSet.x=50;inputSet.y=1082;
  text(board,'Nhãn tab','Tab điều hướng',50,1215,900,27,18,P.dark,true);
  setVariants(board,'Tab / State',[
    ['Selected',P.pale,'Kênh',P.accent],['Default',P.white,'Mọi người',P.muted]
  ],50,1255,230,44);
  text(board,'Nhãn bong bóng','Message bubble',50,1370,900,27,18,P.dark,true);
  setVariants(board,'Message / Sender',[
    ['Mine',P.pale,'Tin nhắn của tôi',P.text],
    ['Other',P.bubble,'Tin nhắn thành viên',P.text]
  ],50,1410,290,72);
  text(board,'Nhãn avatar','Avatar',50,1568,900,27,18,P.dark,true);
  const avatar=figma.createComponent();board.appendChild(avatar);avatar.name='Avatar / Member';avatar.resize(52,52);avatar.x=50;avatar.y=1606;avatar.fills=fill(P.pale);avatar.cornerRadius=26;
  const av=text(avatar,'Chữ viết tắt','HK',0,0,52,52,17,P.accent,true);av.textAlignHorizontal='CENTER';
  text(board,'Quy tắc','Button: 44 px cao, bo góc 12 px  ·  Input: 52 px cao  ·  Avatar: 52 px  ·  Cỡ chữ 13–28 px',130,1613,1090,40,14,P.text);
  text(board,'Nguyên tắc','Tương phản rõ giữa chữ và nền; nút xóa dùng màu riêng; trạng thái lỗi có viền và thông báo bằng chữ.',50,1725,1170,50,14,P.muted);
  const existingColors=await figma.getLocalPaintStylesAsync();
  for(const [name,value] of colors){if(!existingColors.some(s=>s.name==='HKchat/'+name)){const s=figma.createPaintStyle();s.name='HKchat/'+name;s.paints=fill(value);}}
  const existingText=await figma.getLocalTextStylesAsync();
  for(const [name,size,bold] of [['Heading',28,true],['Body',16,false],['Label',13,false]]){
    if(!existingText.some(s=>s.name==='HKchat/'+name)){const s=figma.createTextStyle();s.name='HKchat/'+name;s.fontName=bold?F.bold:F.regular;s.fontSize=size;}
  }
  return page;
}
function screenMap(page){
  const map={};
  for(const child of page.children){if(child.type==='FRAME'){const match=/^(\d\d) \/ /.exec(child.name);if(match)map[match[1]]=child;}}
  return map;
}
function node(screen,name){return screen.children.find(n=>n.name===name);}
async function link(from,name,to){
  if(!from||!to)return false;
  const n=node(from,name);if(!n)return false;
  await n.setReactionsAsync([{trigger:{type:'ON_CLICK'},actions:[{type:'NODE',navigation:'NAVIGATE',destinationId:to.id,transition:{type:'DISSOLVE',easing:{type:'EASE_OUT'},duration:0.18}}]}]);
  return true;
}
async function prototype(){
  const page=figma.root.children.find(p=>p.type==='PAGE'&&p.name==='HKchat – Thiết kế đầy đủ (editable)');
  if(!page)throw new Error('Không thấy trang 18 màn hình HKchat');
  await figma.setCurrentPageAsync(page);await page.loadAsync();
  const s=screenMap(page);if(Object.keys(s).length<18)throw new Error('Trang thiết kế chưa có đủ 18 frame');
  const L=[
    ['01','Nút xác thực / nền','04'],['01','Nút xác thực / chữ','04'],['01','Chuyển biểu mẫu','02'],
    ['01','Địa chỉ server / nền','03'],
    ['02','Nút xác thực / nền','04'],['02','Nút xác thực / chữ','04'],['02','Chuyển biểu mẫu','01'],
    ['03','Nút xác thực / nền','01'],['03','Chuyển biểu mẫu','02'],
    ['04','Tab / Mọi người','07'],['04','Tab / Tìm kiếm','15'],['04','Nút tạo kênh / nền','05'],
    ['04','Kênh / General / tên','09'],['04','Kênh / Random / tên','09'],['04','Kênh / Đồ án chuyên ngành / tên','09'],
    ['04','Kênh / hk_test_channel / tên','06'],['04','Kênh / hk_test_channel / mở','06'],['04','Nút điều hướng','18'],
    ['05','Nút tạo kênh / nền','09'],['05','Nút tạo kênh / chữ','09'],['05','Tab / Mọi người','07'],
    ['06','Kênh / hk_test_channel / mở','09'],['06','Tab / Kênh','04'],
    ['07','Tab / Kênh','04'],['07','Tab / Tìm kiếm','15'],['07','Thành viên Khải / tên','08'],['07','Thành viên Khải / mở','08'],
    ['08','Nút điều hướng','07'],['08','Nút Gửi / nền','08'],
    ['09','Nút điều hướng','04'],['09','Tin Đạt / bong bóng','13'],['09','Tin Đạt / nội dung','13'],
    ['09','Tin Đạt / tác giả','12'],
    ['10','Nút Gửi / nền','09'],['10','Thanh trả lời / hủy','09'],['11','Nút Lưu / nền','09'],['11','Thanh sửa / hủy','09'],
    ['12','Bộ chọn cảm xúc / 👍','09'],['12','Bộ chọn cảm xúc / ❤️','09'],
    ['13','Hộp thoại / Trả lời / nền','10'],['13','Hộp thoại / Sửa / nền','11'],['13','Hộp thoại / Thêm / nền','14'],['13','Hộp thoại / Hủy / nền','09'],
    ['14','Hộp thoại / Hủy / nền','09'],['14','Hộp thoại / Xóa / nền','09'],
    ['15','Nút tìm kiếm / nền','16'],['15','Tab / Kênh','04'],['15','Tab / Mọi người','07'],
    ['16','Kết quả 1 / nền','17'],['16','Kết quả 1 / nội dung','17'],['16','Tab / Kênh','04'],
    ['17','Nút điều hướng','16'],['17','Tin Đạt / bong bóng','13'],
    ['18','Hộp thoại / Hủy / nền','04'],['18','Hộp thoại / Đăng xuất / nền','01']
  ];
  let done=0;const errors=[];const edges={};
  for(const [a,n,b] of L){
    try{
      if(await link(s[a],n,s[b])){
        done++;
        (edges[a]??=[]).push(b);
      }else errors.push(a+' / '+n);
    }catch(error){errors.push(a+' / '+n+': '+String(error));}
  }
  const reached=new Set(['01']);const queue=['01'];
  while(queue.length){const from=queue.shift();for(const to of edges[from]||[]){if(!reached.has(to)){reached.add(to);queue.push(to);}}}
  return {page,count:done,expected:L.length,reached:[...reached].sort(),errors};
}
async function main(){
  await Promise.all([figma.loadFontAsync(F.regular),figma.loadFontAsync(F.bold)]);
  await designSystem();
  const result=await prototype();
  figma.currentPage.selection=[result.page.children.find(n=>n.type==='FRAME'&&n.name.startsWith('01 /'))];
  figma.viewport.scrollAndZoomIntoView(figma.currentPage.selection);
  figma.notify('HKchat: '+result.count+'/'+result.expected+' liên kết; '+result.reached.length+'/18 màn hình có thể đi từ Flow 1.'+(result.errors.length?' Lỗi đầu: '+result.errors[0]:''),{timeout:30000,error:result.errors.length>0||result.reached.length<18});
  figma.closePlugin();
}
main().catch(error=>{console.error(error);figma.notify('Lỗi: '+String(error),{error:true,timeout:30000});figma.closePlugin();});

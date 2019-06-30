drop table if exists user;
create table user (
    id integer primary key autoincrement,
    name text not null,
    passwd text not null,
    phone integer not null,
    addr integer not null,
    time integer not null
);

drop table if exists goods;
create table goods (
    id integer primary key autoincrement,
    name text not null,
    pic text not null,
    price integer not null,
    discount integer default 0,
    num integer default 0
);

drop table if exists advice;
create table advice (
    id integer primary key autoincrement,
    contact text,
    content text not null,
    time integer not null
);

drop table if exists cart;
create table cart (
    id integer primary key autoincrement,
    username text,
	contact text not null,
    list text not null,
    note text,
    comment text,
    time integer not null,
    deliver text not null,
    pickup text not null,
    dtime text not null,
    ptime text not null,
	wtime text,
	state integer default 0
);

/************NEW START**********************/
drop table if exists user1;
create table user1 (
    id integer primary key autoincrement,
    name text not null,
    passwd text not null,
    phone test not null,
    address test ,
    school test not null,
    u_type test,
    time integer not null
);


Insert into





drop table if exists merchant;
create table merchant (
    id integer primary key autoincrement,
    m_id integer not null,
    merchant text not null,
    m_name text not null,
    m_passwd text not null,
    scope text
);
6|1101|洁丽雅来|FDNJLYL|FDNJLYL|复旦大学|5
insert into merchant(m_id,merchant,m_name,m_passwd, scope) value(1000,’约瑟芬精奢洗护馆’,’SJTUXH’,’SJTUXH’)




insert into user(name,passwd,phone,school,u_type,time) values(‘Elvin’,’liyi19950920’,’18217237150’,’上海交通大学(徐汇)’,’普通用户’,1505650309)






drop table if exists membership;
create table membership (
    id integer primary key autoincrement,
    l_id integer not null,
    level_name text ,
    level_discount_name test,
    level_discount double
);


VIP会员 八折优惠


insert into membership(l_id,level_name,level_discount_name,level_discount) values(1,'普通用户','',0);
insert into membership(l_id,level_name,level_discount_name,level_discount) values(2,'超级会员','八折优惠',0.8);
insert into membership(l_id,level_name,level_discount_name,level_discount) values(3,'VIP会员','八折优惠',0.8);
insert into membership(l_id,level_name,level_discount_name,level_discount) values(4,'至尊会员','八折优惠',0.8);


insert into merchant(m_id,merchant,m_name,m_passwd,scope) values(1,'UCC国际洗衣','UCC','SJUCC','松江一期');
insert into merchant(m_id,merchant,m_name,m_passwd,scope)values(2,'韩式良家','SJHSLJ','SJHSLJ','松江四期');


drop table if exists user_vip;
create table user_vip (
    id integer primary key autoincrement,
    submit_time TimeStamp
    use_time text
    ip text
    source text
    source_detail text
    school  text
    prefession text
    grade  text
    gender text
    phone text
);
insert into user_vip(submit_time,use_time,ip,source,source_detail,school,prefession,grade,gender,phone) values('2017/9/14 19:16:53','67秒','112.65.48.10(上海-上海)','手机提交','微信','上海财经大学','法硕','研一','2','18621066095');

/*****

在这个表里创建一个表：
CREATE TABLE time([ID] INTEGER PRIMARY KEY,
[IDCardNo] VARCHAR (50),
[CreatedTime] TimeStamp NOT NULL DEFAULT CURRENT_TIMESTAMP);
插入数据：
INSERT INTO time([IDCardNo]) VALUES('aaa');
查看：
select * from time;
结果是
1|aaa|2011-10-6 06:48:51
这时会发现这个时间并不是系统的时间，而世界时间，怎么处理呢？

CREATE TABLE time([ID] INTEGER PRIMARY KEY,[IDCardNo] VARCHAR (50),[CreatedTime] TimeStamp NOT NULL DEFAULT (datetime('now','localtime')));

再次插入数据

INSERT INTO time([IDCardNo]) VALUES('aaa');

查看：
1|aaa|2011-10-6 13:05:51
这样就和系统的本地时间对应了。


 */






drop table if exists commodity;
create table commodity (
    id integer primary key autoincrement,
    c_id integer not null,
    c_name text not null,
    imgURL text,
    c_type integer
);

insert into commodity(c_id,c_name,imgURL,c_type) values(1,'西服上衣','http://7xitj5.com1.z0.glb.clouddn.com/static/img/1西服上衣 拷贝.jpg',0);
update  commodity set imgURL=replace(imgURL,'`static/img/pillowcase.jpg','static/img/pillowcase.jpg')

insert into commodity(c_id,c_name,imgURL,c_type) values(2,'西裤','http://7xitj5.com1.z0.glb.clouddn.com/static/img/2西裤 拷贝.jpg',0);

update commodity set imgURL=replace(imgURL,'static/img/23枕套 拷贝.jpg','static/img/pillowcase.jpg') where id=397;



 update commodity set imgURL='static/img/pillowcase.jpg' where id=397;




drop table if exists tariff;
create table tariff (
    id integer primary key autoincrement,
    m_id integer not null,
    c_id integer not null,
    price integer,
    discount integer,
    promotion integer
    disPrice integer
);
//UCC
insert into tariff(m_id,c_id,price,discount,promotion) values(1,1,20,0,14);
insert into tariff(m_id,c_id,price,discount,promotion) values(1,2,15,0,9);



update tariff set promotion =9 where c_id =1

update tariff set price =15 where c_id=2

//韩式
insert into tariff(m_id,c_id,price,discount,promotion) values(2,1,30,0,20);
insert into tariff(m_id,c_id,price,discount,promotion) values(2,2,10,0,1);


select c_name,imgURL from commodity


/*
select scope,merchant,c_name,imgURL,price,promotion from merchant m left join tariff t on m.m_id = t.m_id  left join commodity c  on  t.c_id=c.c_id where scope='松江一期'

松江一期|UCC国际洗衣|西服上衣|20|14
松江一期|UCC国际洗衣|西裤|15|9
松江四期|韩式良家|西服上衣|30|20
松江四期|韩式良家|西裤|10|1

*/


drop table if exists cart;
create table cart (
    id integer primary key autoincrement,
    username text,   用户名
	  contact text not null,   联系方式
    list text not null,    购物链表
    note text,      备注
    comment text,   评论
    time integer not null,  时间
    deliver text not null,  分发
    pickup text not null,
    dtime text not null,
    ptime text not null,
	wtime text,
	state integer default 0   状态
);



username, contact, list, note, comment, time, deliver, pickup, dtime, ptime, wtime, state

username phone list      note comment   time  deliver  pickup dtime ptime wtime  state  scope



drop table if exists cart1;
create table cart1 (
id integer primary key autoincrement,
username text,
phone text not null,
list text not null,
note text,
comment text,
time integer not null,
deliver text not null,
pickup text not null,
dtime text not null,
ptime text not null,
wtime text,
state integer default 0,

 test,
oldPrice double,
vipPrice double
);


select c.id as 'id',state,list,c.time as 'time',deliver,dtime,c.phone as 'phone',note, comment from cart1 c left join user1 u on c.phone=u.phone;



update cart set oldPrice=15 where phone='15021165098' and id=195;

select * from cart where phone='18217505831';

select * from cart where phone='18097717636' and id=205

select count(*)from cart where substr(dtime,1,4)='9-20' and scope='上海交通大学'








select c.id  id,state,list,c.time time,deliver,dtime,name,c.phone phone,u_type,note, comment from cart1 c left join user1 u on c.phone=u.phone where c.time>? order by ID desc', [int(time.time())-604800]

$(document).ready(function(){

	//从/RandomSelect中抓取随机抽取的20个单词及翻译
	$.get("/RandomSelect",function(data){
		var allWords=data;
		//用split函数根据","将字符串切割
		var wordList=allWords.split(",",40);
		//定义英文单词数组和中文翻译数组并赋值
		var engList=new Array(20);
		var chnList=new Array(20);
		for (var i=0;i<wordList.length;i++)
		{
			if (i%2==0)
			{
				engList[i/2]=wordList[i];
			}
			else
				chnList[(i-1)/2]=wordList[i];
		}
		//将原有的数组复制到两个新数组进行洗牌
		var engRandomList=engList.slice();
		var chnRandomList=chnList.slice();
		//将英文单词数组和中文数组打乱顺序，算法来源http://blog.csdn.net/kongjiea/article/details/48497917
		engRandomList.sort(function(){return 0.5 - Math.random()});
		chnRandomList.sort(function(){return 0.5 - Math.random()});
		//将选取好的词语显示在html上
		$(".eng").each(function(index){
			$(this).html(engRandomList[index]);		
		});
		$(".chn").each(function(index){
			$(this).html(chnRandomList[index]);		
		});
		//定义函数以判断两个字符串是否为对应的中英文单词，英文在前，中文在后
		function isPair(eng,chn){
			//寻找英文单词在engList中的序号
			for (var j=0;j<engList.length;j++)
			{
				if (engList[j]==eng)
				{
					break
				}
			}
			//判断中文单词是否是对应的chnList中的元素
			return chnList[j]==chn
		}
		//根据点击事件进行判断
		//temp用于记录当前被选中的英语和汉语内容，初始为None
		var tempEng="";
		var tempChn="";
		//tempQ用于记录当前被选中的jQuery对象，初始指向p
		var tempQ=$("p");
		//status用于记录被选中的是英语(0)还是汉语(1)，初始情况为-1
		var status=-1;
		$(".eng").click(function(){
			tempEng=$(this).html();
			switch(status){
			case -1:
				tempQ=$(this);
				$(this).css("background-color","grey");
				status=0;
				break;
			case 0:
				alert("不可以连续选择两个英语单词，上一次选择已被覆盖");
				tempQ.css("background-color","yellow");
				$(this).css("background-color","grey");
				tempQ=$(this);
				break;
			case 1:
				//检查目前存储的内容是否正确，无论正确与否缓存内容均被清空
				if (isPair(tempEng,tempChn))
				{
					alert("选择正确！");
					tempQ.fadeOut("fast");
					$(this).fadeOut("fast");
				}
				else
				{
					alert("选择错误！");
					tempQ.css("background-color","green");
				}	
				tempEng="";
				tempChn="";
				tempQ=$("p");
				status=-1;
				break;
			}
		});
		$(".chn").click(function(){
			tempChn=$(this).html();
			switch(status){
			case -1:
				tempQ=$(this);
				$(this).css("background-color","grey");
				status=1;
				break;
			case 1:
				alert("不可以连续选择两个汉语单词，上一次选择已被覆盖");
				tempQ.css("background-color","green");
				$(this).css("background-color","grey");
				tempQ=$(this);
				break;
			case 0:
				//检查目前存储的内容是否正确，无论正确与否缓存内容均被清空
				if (isPair(tempEng,tempChn))
				{
					alert("选择正确！");
					tempQ.fadeOut("fast");
					$(this).fadeOut("fast");
				}
				else
				{
					alert("选择错误！");
					tempQ.css("background-color","yellow");				
				}
				tempEng="";
				tempChn="";
				tempQ=$("p");
				status=-1;
				break;
			}
		});
	});
});

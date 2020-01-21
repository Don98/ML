#KMP算法

其实这一个算法是用来解决给个模板p，在s中找到匹配的问题的算法。

然后这里先不谈这个，先解决最短回文串的问题，就是在leetcode214的问题，在前面增加最少的字符串让整体变成回文的。

首先是暴力法，是O（n^2）的方法。

然后第二个方法是双指针的方法，一个从左指针，一个右指针，一旦到两个指针的内容相等的话就左指针右移，直到右指针到头为止，如果结束后左指针在字符串的最后这意味着这个字符串是回文的，如果不是，那么回文串在0到左指针的范围内，根据这个原理实现双指针+递归，代码如下：

	class Solution {
	public:
	    string shortestPalindrome(string s) {
	        int i = 0;
	        for(int j = s.length()-1;j >= 0;j--){
	            if(s[i] == s[j])
	                i++;
	        }
	        if(i == s.length())
	            return s;
	        string result = "";
	        result = s.substr(i);
	        reverse(result.begin(),result.end());
	        return result + shortestPalindrome(s.substr(0,i)) + s.substr(i);
	    }
	};


<center>
<img src="pic/12.png">

</center>


然后就是使用KMP算法的思想,其实就是什么呢，主要是匹配串p里面要有重复的，比如在"BBC ABCDAB ABCDABCDABDE"中找到"ABCDABD"这一个字符串，然后具体是怎么做的呢？

比如当进行如下匹配的时候：

<center>
<img src="pic/13.png">

</center>

会发现在D处匹配不了，如果我们这个时候把p串向后移动一格又会浪费了p串中对比过的信息，于是我们可以直接进行下面的位置，

<center>
<img src="pic/14.png">

</center>

因为我们之前已经匹配过了，所以可以直接跳。

我们构建如下的表格：
<center>
<img src="pic/15.png">

</center>

本质就是不断找到A、AB、ABC、ABCD、……、ABCDABD的相同的真前缀和真后缀。

然后就是构建表格的一个伪代码：

	/* P 为模式串，下标从 0 开始 */
	void GetNext(string P, int next[])
	{
	    int p_len = P.size();
	    int i = 0;   // P 的下标
	    int j = -1;  
	    next[0] = -1;
	
	    while (i < p_len)
	    {
	        if (j == -1 || P[i] == P[j])
	        {
	            i++;
	            j++;
	            next[i] = j;
	        }
	        else
	            j = next[j];
	    }
	}

然后我们这里借助构建表格的思想进行匹配，本质就是找到相同的真前缀和真后缀，所以我们在这里将原本的字符串比如“aacecaaa”反转后拼回到原本的字符串，如：“aacecaaa#aaacecaa”，“#”号是将前后两个分割出来。

最后的代码答案：
	
	class Solution {
	public:
	    string shortestPalindrome(string s) {
	        string rev(s);
	        reverse(rev.begin(),rev.end());
	        int s_length = s.length();
	        string new_s = s + "#" + rev;
	        int n = new_s.length();
	        int i = 0,j = -1;    
	        vector<int> f(n+1, 0);
	        f[0]=-1;
	        while(i < n){
	            if(j == -1 || new_s[i] == new_s[j]){
	                i++;
	                j++;
	                f[i] = j;
	            }
	            else
	                j = f[j];
	        }
	        string result = "";
	        for(int i = 0;i < s_length - f[n];i++)
	            result += s[s_length - i - 1];
	        return result + s;
	    }
	};

<center>
<img src="pic/11.png">

</center>

这个参考地址内提到的“可能有的读者会疑惑”的内容，说到底，我现在好不知道疑惑在哪里。。。先保留着。

参考网址地址：[https://segmentfault.com/a/1190000008575379](https://segmentfault.com/a/1190000008575379)
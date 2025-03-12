# prototypR

Prototype Pollution Detector Tool

- This tool is use the following research: [s1r1us PP Research](https://blog.s1r1us.ninja/research/PP)




## Example Usage

Implement and example vulnerable fragment of code [BlackFan Client-Side Prototype Pollution](https://github.com/BlackFan/client-side-prototype-pollution/blob/master/pp/jquery-parseparam.md)

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
<script src="https://gist.githack.com/jhjguxin/10971155/raw/f5a8625d868cca305387252dd3293864868d455d/jquery.parseparams.js"></script>
<script>
  $.parseParams(location.href);
</script>
```

Then execute the tool which found Prototype pollution:


```bash
python3 prototyper.py -u "http://127.0.0.1:9001/parseparam.html?foo=bar"                                                          
[+] Prototype Pollution found on URL: http://127.0.0.1:9001/parseparam.html?foo=bar&x.__proto__.edcbcab=edcbcab
[+] Prototype Pollution found on URL: http://127.0.0.1:9001/parseparam.html?foo=bar&__proto__.baaebfc=baaebfc
[+] Prototype Pollution found on URL: http://127.0.0.1:9001/parseparam.html?foo=bar&constructor.prototype.cfbacfd=cfbacfd

```

Check The result:

- Open a new browser tab
- Navigate to the affected url copied from the tool result
- Open Browser Console [`F12`]
- Execute: `Object.prototype`

![image](https://github.com/user-attachments/assets/34051295-a7f6-4e37-89dc-5b379c7b71ee)


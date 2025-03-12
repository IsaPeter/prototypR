# PrototypR

Prototype Pollution Detector Tool

- This tool is use the following research: [s1r1us PP Research](https://blog.s1r1us.ninja/research/PP)
- The prototype_checker.js file was copied from: [cspp-tools](https://github.com/BlackFan/cspp-tools/blob/main/prototype_checker/prototype_checker.js)




## Example Usage

Implement an example vulnerable fragment of code [Link](https://github.com/BlackFan/client-side-prototype-pollution/blob/master/pp/jquery-parseparam.md)

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


![image](https://github.com/user-attachments/assets/b220220a-a3df-4d97-9bb3-cb0cc65646bc)

-----

# PPSignature

Signature based detection

**Check Single URL**

```bash
python3 ppsignature.py -u "https://raw.githack.com/cowboy/jquery-bbq/8e0064ba68a34bcd805e15499cb45de3f4cc398d/jquery.ba-bbq.js"
[*] Potentially Vulnerable JS found! (jQuery BBQ (deparam) Prototype Pollution)
[*] Potentially Vulnerable JS found! (deparam Prototype Pollution)
```

**Check URL List**

```bash
python3 ppsignature.py -ul /tmp/urls                                                                                                               
[*] Potentially Vulnerable JS found! (davis.js Prototype Pollution)
[*] Potentially Vulnerable JS found! (jQuery Sparkle Prototype Pollution)
[*] Potentially Vulnerable JS found! (jQuery BBQ (deparam) Prototype Pollution)
[*] Potentially Vulnerable JS found! (deparam Prototype Pollution)
```






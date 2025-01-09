TryHackMe's **c4ptur3-th3-fl4g** is the easy-level room to practice decoding messages, analyzing a spectrogram, steganography. This writeup will go cover everything required to complete the room. 

I will provide detailed knowledge about each topic and the tools I used to solve the challenges.

# Task 1: Translation & Shifting
##### 1. Message One
We can easily know the answer of the encoded message because it simply converts some letters with numbers.

##### 2. Message Two
The message is made up of 0s and 1s, we know that it's binary. And I will using [CyberChef](https://cyberchef.org/) to translate it. Plugging into CyberChef and using the "From Binary" recipe we can get the decoded message.

![Decoded Message](../images/c4ptur3-th3-fl4g-message2.png)

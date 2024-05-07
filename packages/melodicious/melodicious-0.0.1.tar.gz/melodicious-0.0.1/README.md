
<br>
<div align="center" class= "main"> 
  <img src="materails/img/logo.png" width="300" height="300" style="border-radius: 10px"/>
  <h1 style="letter-spacing: 2.5px;font-weight: lighter">Melodicious AI</h1>
<a href="https://github.com/DarkMakerofc"><img title="Creator" src="https://img.shields.io/badge/Creator-Cropsun-purple.svg?style=for-the-badge&logo=github"></a>
<br><br><br>
</div>

## License Agreement

<div style="font-weight: lighter;font-size: 13px;letter-spacing: 0.6px">
Any use for borken human artist or fake stream are not allowed here
</div>
<br><hr>

## What's this

<div style="font-weight: lighter;font-size: 13px;letter-spacing: 0.6px">
An easy-to-use API for generating music
</div>
<br><hr>

## More details

<div style="font-weight: lighter;font-size: 13px;letter-spacing: 0.6px">
Your can generate your own music in high-solution method we call "ai-midi"
even you can sing and render your voice to professional vocalist
</div>
<br><hr>

## How to setup

```ssh
pip install melodicious
```

<br><hr>

## For example

```python
import melodicious

client = melodicious.APIClient(base_url="", username="", usertoken="", callEndpoint="", data="")

response = client.playing()

print(response)
```

<br><hr>


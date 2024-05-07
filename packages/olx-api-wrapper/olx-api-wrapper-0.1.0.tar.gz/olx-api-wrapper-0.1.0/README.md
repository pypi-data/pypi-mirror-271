<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Pawikoski/olx-api-wrapper">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">OLX Api Wrapper</h3>

  <p align="center">
    Simple client for OLX Developer API written in Python
    <br />
    <a href="https://github.com/Pawikoski/olx-api-wrapper"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Pawikoski/olx-api-wrapper">View Demo</a>
    ·
    <a href="https://github.com/Pawikoski/olx-api-wrapper/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/Pawikoski/olx-api-wrapper/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![OLX API Wrapper Image][product-image]](https://github.com/Pawikoski/olx-api-wrapper)

OLX API Wrapper: Easy Solution for Working with OLX. With this Python library you can quickly fetch user data, handle adverts with simple CRUD operations, and seamlessly integrate with the OLX API. Simplify your development process and focus on building your app hassle-free.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python]][Python-url]
* [![requests][requests]][requests-url]
* [![dacite][dacite]][dacite-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

In order to use OLX Api you nned to sign in at OLX Developer Portal and create an App.
More details: https://developer.olx.pl/articles/getting-access-to-api

### Prerequisites

To use this API Wrapper you need to copy Client ID and Client Secret. Store them in the safe place. In your code you can use them as enviroment variables, they sholdn't be hardcoded.

### Installation

1. Install `olx-api-wrapper` package
   ```sh
   pip install olx-api-wrapper
   ```
2. In order to get access token you need to authenticate with authorization code. [How to get authorization code?](https://developer.olx.pl/api/doc#section/Authentication/Grant-type:-authorization_code)
   ```python
   from olx import Auth
   auth = Auth(
     client_id="your_client_id",
     client_secret="your_client_secret",
   )
   auth.authenticate(code='authorization_code')
   access_token = auth.access_token
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/Pawikoski/olx-api-wrapper/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - pawikoski@gmail.com

Project Link: [https://github.com/Pawikoski/olx-api-wrapper](https://github.com/Pawikoski/olx-api-wrapper)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Pawikoski/olx-api-wrapper.svg?style=for-the-badge
[contributors-url]: https://github.com/Pawikoski/olx-api-wrapper/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Pawikoski/olx-api-wrapper.svg?style=for-the-badge
[forks-url]: https://github.com/Pawikoski/olx-api-wrapper/network/members
[stars-shield]: https://img.shields.io/github/stars/Pawikoski/olx-api-wrapper.svg?style=for-the-badge
[stars-url]: https://github.com/Pawikoski/olx-api-wrapper/stargazers
[issues-shield]: https://img.shields.io/github/issues/Pawikoski/olx-api-wrapper.svg?style=for-the-badge
[issues-url]: https://github.com/Pawikoski/olx-api-wrapper/issues
[license-shield]: https://img.shields.io/github/license/Pawikoski/olx-api-wrapper.svg?style=for-the-badge
[license-url]: https://github.com/Pawikoski/olx-api-wrapper/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/paweł-stawikowski
[product-image]: images/image.png
[Python]: https://img.shields.io/badge/python-000000?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://python.org/
[dacite]: https://img.shields.io/badge/dacite-20232A?style=for-the-badge&logo=github&logoColor=61DAFB
[dacite-url]: https://github.com/konradhalas/dacite
[requests]: https://img.shields.io/badge/requests-35495E?style=for-the-badge&logo=github&logoColor=4FC08D
[requests-url]: https://github.com/psf/requests

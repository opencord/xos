# ngXosLib

Please see the full documentation here:
http://ngxoslib.wiki.opencord.org/

## Quick Notes

This library has been developer to be used along with the [CORD Project](http://opencord.org/) and in particular to be integrated in [XOS](http://guide.xosproject.org/).

During the process we have developed a set of common bootstrap based UI Component and we decided to release them in the community, that's why you'll find more generated files than you'll need to include also if only the `xosUiComponents.js` is listed in the `bower.json` main section.

## Setup a development environment

The project is managed through Gerrit, you can get it at: https://gerrit.opencord.org/#/admin/projects/ng-xos-lib

Once cloned enter the project folder and execute: `npm run dev`

This command will serve the `dev` folder, and watch files to enable live-reload. It will also watch the files in the `src` folder and inject the new version when changed.

### Build

Before submitting a review on gerrit, it is mandatory to build the code with: `npm run build`.

### Executing tests

You can execute tests in watch mode with: `npm test`. If you are working on a particular component and want to run a single suite of tests you append to the command the name of the file containing the test suite you want to execute, eg: `npm run form`.
To execute tests on the minified code (these are the ones that runs on Jenkins): `npm run test:ci` (but remember to build the code first!).

ESLint is used in this project, to execute it on all the source code: `npm run lint`

## Contributing

Any contribution is welcome and will be supported. Feel free to open issues in this repository or join the OpenCORD [Slack Channel](https://slackin.opencord.org/)

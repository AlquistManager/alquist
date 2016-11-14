# Alquist client

HTML client for Alquist dialogue manager https://github.com/konrajak/alquist

You can test current demo at https://alquistmanager.github.io/alquist-client/?e=https://alquist.herokuapp.com&bot=demo_tel

## Usage
You have to specify which bot you want to interact with by URL parameter ``bot=[bot name]`` or by attaching bot name as path to address like:

    http://127.0.0.1:5000/[bot_name]/

You can change endpoint's address of Alquist dialogue manager by URL paramater ``e=[Alquist endpoint]``.

The default endpoint's value is ``http://localhost:5000/``.

Example: 

    http://localhost:63342/alquist-client/index.html?e=http://localhost:5000/&bot=demo_tel
    
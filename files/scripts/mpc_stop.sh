#!/bin/bash
if [ "$PLAYER_EVENT" == "started" ] || [ "$PLAYER_EVENT" == "playing" ]
then
    /usr/bin/mpc -q stop
fi
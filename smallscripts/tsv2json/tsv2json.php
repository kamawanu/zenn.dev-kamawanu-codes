<?php

$kw = false;

while (($buff = fgets(STDIN)) !== false) {
    $pw = explode("\t", trim($buff));
    if ($kw === false) {
        $kw = $pw;
        continue;
    }
    $tsv = array_combine($kw, $pw);

    foreach (array_keys($tsv) as $key) {
        if ($key[0] == "!") {
            unset($tsv[$key]);
            continue;
        }
        if ($key[0] == "#") {
            $nw = substr($key, 1);
            $tsv[$nw] = intval($tsv[$key]);
            unset($tsv[$key]);
            $key = $nw;
        }
        $kww = explode(".", $key);
        if (count($kww) > 1) {
            unset($pos);
            $pos = & $tsv;
            while (count($kww) > 0) {
                $pos = & $pos[array_shift($kww)];
            }
            $pos = $tsv[$key];
            unset($pos);
            unset($tsv[$key]);
        }
    }

    echo json_encode($tsv) . "\n";
}

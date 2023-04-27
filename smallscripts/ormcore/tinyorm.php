<?php

class tinyorm {

    protected $_before;
    protected $_after;
    protected $_methodmaps = array();

    public function __construct(array $src) {
        $this->_before = $src;
        $this->_methodmaps = array();
    }

    public function use_as(string $name, string $method): void {
        if (!isset($this->_after[$name])) {
            $this->_methodmaps[$name] = $method;
            $this->_after["$method.$name"] = static::decode($method, $this->_before[$name]);
            $this->_after[$name] = $this->_before[$name];
        }
    }

    protected static function encode(string $method, $value) {
        return static::{"encode_$method"}($value);
    }

    protected static function decode(string $method, $value) {
        return static::{"decode_$method"}($value);
    }

    protected static function decode_json(string $str): array {
        return json_decode($str, TRUE);
    }

    protected static function encode_json($str): string {
        return json_encode($str);
    }

    public function & __get(string $name) {
        if (isset($this->_methodmaps[$name])) {
            $method = $this->_methodmaps[$name];
            return $this->_after["$method.$name"];
        }
        if (!isset($this->_after[$name])) {
            $this->_after[$name] = $this->_before[$name];
        }
        if (!is_string($this->_after[$name])) {
            throw new \Exception("serialize first for $name");
        }
        return $this->_after[$name];
    }

    public function __set(string $name, $value) {
        if (isset($this->_methodmaps[$name])) {
            $method = $this->_methodmaps[$name];
            $this->_after["$method.$name"] = $value;
        } else {
            $this->_after[$name] = $value;
        }
    }

    public function get_before(): array {
        return $this->_before;
    }

    public function get_after(): array {
        $r = $this->_after;
        foreach ($this->_methodmaps as $name => $method) {
            $r[$name] = $this->_after[$name] = static::encode($method, $this->_after["$method.$name"]);
            unset($r["$method.$name"]);
        }
        return $r;
    }

    public function get_differ(): array {
        return array_diff($this->_before, $this->_after);
    }

}

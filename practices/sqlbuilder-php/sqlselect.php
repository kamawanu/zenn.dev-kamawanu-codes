<?php

require "if.php";
require "sqlparts.php";


abstract class sqlselect
{
    use haswhere;
    use hasfrom;
    use hasregion;

    var $columns = "*";
    var $_order = false;
    #var $_offset = false;
    protected $owner = null;

    function __construct($name, dbowner &$owner)
    {
        $this->_name = $name;
        $this->where = array();
        $this->_order = array();
        $this->owner = &$owner;
    }
    public function &order($cols)
    {
        $this->_order[] = $cols;
        return $this;
    }
    public function __toString()
    {
        $sql = sprintf("select %s from %s ", $this->columns, $this->_name);
        if (count($this->where) > 0) {
            $sql .= " where " . join(" and ", $this->where);
        }
        if (count($this->_order) > 0) {
            $sql .= " order by " . join(",", $this->_order);
        }
        if ($this->_limit !== false && $this->_offset) {
            $sql .= sprintf(" offset %d,%d", $this->_offset, $this->_limit);
        }
        return $sql;
    }
}

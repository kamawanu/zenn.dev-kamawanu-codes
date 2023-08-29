<?php

require "if.php";
require "sqlparts.php";

abstract class sqldelete
{
    use haswhere;
    use hasregion;
    use hasfrom;

    function __construct($name)
    {
        $this->_name = $name;
        $this->where = array();
        $this->_limit = 1;
    }

    function __toString()
    {
        $sql = sprintf("delete from %s", $this->_name);
        if (count($this->where) > 0) {
            $sql .= " where " . join(" and ", $this->where);
        }
    }
}

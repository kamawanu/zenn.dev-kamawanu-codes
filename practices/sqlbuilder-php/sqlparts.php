<?php

trait haswhere
{
    var $where;

    abstract function quotevalue($value);

    public function &where($sqlstr, $value = null)
    {
        $this->where[] = str_replace("?", $this->owner->quotevalue($value), $sqlstr);
        return $this;
    }
}

trait hasfrom
{
    var $_name;
    public function &from($cols)
    {
        $this->_name = $cols;
        return $this;
    }
}

trait hasregion
{
    var $_limit;
    var $_offset;
    public function &limit($limit, $offset)
    {
        $this->_limit = $limit;
        $this->_offset = $offset;
        return $this;
    }
}
